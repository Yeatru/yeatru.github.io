#!/usr/bin/env node
// ---------------------------------------------------------------------------
// Generate a PBKDF2-SHA-256 admin password hash and a random session secret.
// Output values are directly pasteable into Cloudflare Pages environment
// variables (Project → Settings → Environment variables → Production):
//
//   ADMIN_USERNAME       例如  Yeatru
//   ADMIN_PASSWORD_HASH  由本脚本生成的 pbkdf2_sha256$...$...$... 字符串
//   ADMIN_SECRET         由本脚本生成的 48+ 字节 URL-safe base64 字符串
//
// Requires Node.js >= 16 (uses the Web Crypto API, globalThis.crypto).
//
// Usage:
//   node scripts/generate-admin-hash.js <username> <password> [iterations]
//   node scripts/generate-admin-hash.js -p                  # prompt via stdin
//   node scripts/generate-admin-hash.js                     # show help + verify
// ---------------------------------------------------------------------------

const wc = (() => {
    // Node.js exposes Web Crypto via require('crypto').webcrypto (Node 15+).
    // Browsers / Workers use globalThis.crypto. Pick whichever is available.
    let webcrypto;
    try { webcrypto = require('crypto').webcrypto; } catch (_) { webcrypto = null; }
    if (!webcrypto && globalThis.crypto && globalThis.crypto.subtle) webcrypto = globalThis.crypto;
    if (!webcrypto || !webcrypto.subtle || typeof webcrypto.getRandomValues !== 'function') {
        throw new Error('Web Crypto API not available. Upgrade Node.js to >= 16 or run in a browser/Worker.');
    }
    return webcrypto;
})();
const subtle = wc.subtle;
const getRandomValues = (buf) => wc.getRandomValues(buf); // bind Crypto as `this`
const ITERATIONS_DEFAULT = 600000;
const SALT_BYTES = 16;
const HASH_BYTES = 32; // SHA-256
const SECRET_BYTES = 48; // ≥ 256 bits of entropy for HMAC signing key

function b64enc(bytes) {
    // URL-safe base64 without padding (matches functions/_shared/auth.js).
    let bin = '';
    for (let i = 0; i < bytes.length; i++) bin += String.fromCharCode(bytes[i]);
    return btoa(bin).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

function b64dec(s) {
    s = String(s).replace(/-/g, '+').replace(/_/g, '/');
    while (s.length % 4) s += '=';
    const bin = atob(s);
    const out = new Uint8Array(bin.length);
    for (let i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
    return out;
}

function randomBytes(n) {
    const buf = new Uint8Array(n);
    getRandomValues(buf);
    return buf;
}

async function derive(passwordText, saltBytes, iterations) {
    const pwKey = await subtle.importKey(
        'raw',
        new TextEncoder().encode(passwordText),
        { name: 'PBKDF2' },
        false,
        ['deriveBits']
    );
    const bits = await subtle.deriveBits(
        { name: 'PBKDF2', salt: saltBytes, iterations, hash: 'SHA-256' },
        pwKey,
        HASH_BYTES * 8
    );
    return new Uint8Array(bits);
}

async function verify(passwordText, formatted) {
    const m = /^pbkdf2_sha256\$(\d+)\$([A-Za-z0-9_-]+)\$([A-Za-z0-9_-]+)$/.exec(formatted);
    if (!m) return false;
    const iterations = parseInt(m[1], 10);
    const salt = b64dec(m[2]);
    const expected = b64dec(m[3]);
    const got = await derive(passwordText, salt, iterations);
    if (got.length !== expected.length) return false;
    let diff = 0;
    for (let i = 0; i < got.length; i++) diff |= got[i] ^ expected[i];
    return diff === 0;
}

async function generate(username, password, iterations) {
    iterations = iterations || ITERATIONS_DEFAULT;
    if (iterations < 100000) {
        console.warn(`[warn] iterations=${iterations} is below 100000; prefer >= 310000 for NIST SP 800-132 compliance.`);
    }
    const salt = randomBytes(SALT_BYTES);
    const hash = await derive(password, salt, iterations);
    const formatted = `pbkdf2_sha256$${iterations}$${b64enc(salt)}$${b64enc(hash)}`;
    const ok = await verify(password, formatted);
    if (!ok) {
        throw new Error('Self-check failed: freshly-generated hash did not verify against input password.');
    }
    const secret = b64enc(randomBytes(SECRET_BYTES));
    return { username, formatted, secret, iterations };
}

function usage() {
    console.log(`
Cloudflare Pages 管理员账号凭证生成器
======================================

用法:
  1) 直接传参:
       node scripts/generate-admin-hash.js <用户名> <密码> [迭代次数]

  2) 交互式(不泄露密码到 shell history):
       node scripts/generate-admin-hash.js -p

  3) 仅生成一个随机 SESSION_SECRET(用于轮换密钥):
       node scripts/generate-admin-hash.js --gen-secret

  4) 验证某个现有哈希是否能通过(自检/排查):
       node scripts/generate-admin-hash.js --verify "<pbkdf2_sha256$...$...$...>"

输出含义:
  ADMIN_USERNAME         — 登录时使用的用户名 (明文,推荐 Yeatru 或更独特的字符串)
  ADMIN_PASSWORD_HASH    — PBKDF2 加盐哈希字符串,Cloudflare Pages 环境变量保存
  ADMIN_SECRET           — HMAC-SHA256 会话 cookie 签名密钥,每台部署/每次轮换都要换新

部署步骤 (粘贴到 Cloudflare Pages → Settings → Environment variables):
  1. 访问 https://dash.cloudflare.com/ → Workers & Pages → yeatru.github.io → Settings
  2. 找到 Environment variables,切换到 Production 环境
  3. 添加 3 条变量 (勾选 "Encrypt" 选项以加密保存):
       ADMIN_USERNAME       = (上面的用户名, 例如 Yeatru)
       ADMIN_PASSWORD_HASH  = (上面 pbkdf2_sha256$... 整段)
       ADMIN_SECRET         = (上面 64 字符长的随机串)
  4. 点击 "Save and deploy" (或重新部署)让 Functions 读到新变量。
     注意: Functions 不支持运行时读取 _headers,必须通过 env.<NAME>。

安全提示:
  * 迭代次数默认 ${ITERATIONS_DEFAULT}。2024 年 OWASP 推荐 PBKDF2-HMAC-SHA256 >= 310000;
    600000 对 Cloudflare Functions (单函数 ≤ 50ms CPU) 略紧,实测 40-70ms 仍在可接受范围。
    如遇偶尔 500,可降为 310000 仍在安全边界内。
  * ADMIN_SECRET 至少要 32 字节随机熵,本脚本提供 48 字节(384 bit)。
  * 更改密码后,把 ADMIN_SECRET 一起换一个新的值,可让所有已有会话立即失效。
  * 旧的前端 localStorage key (yeatruAdminLoggedIn) 会被前端新代码在加载时清除,
    不需要手动迁移。
`);
}

async function readStdin(prompt) {
    return new Promise((resolve) => {
        const rl = require('readline').createInterface({
            input: process.stdin,
            output: process.stdout
        });
        rl.question(prompt, (line) => { rl.close(); resolve(line); });
    });
}

async function main(argv) {
    const args = argv.slice(2);
    const first = args[0];

    if (!first || first === '-h' || first === '--help') {
        usage();
        process.exit(0);
    }

    if (first === '--gen-secret') {
        console.log(b64enc(randomBytes(SECRET_BYTES)));
        process.exit(0);
    }

    if (first === '--verify') {
        const hashStr = args[1];
        if (!hashStr) { console.error('missing hash argument'); process.exit(2); }
        const readline = require('readline');
        const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
        rl.question('Password to verify: ', async (pw) => {
            rl.close();
            const ok = await verify(pw, hashStr);
            console.log(ok ? 'OK (password matches)' : 'FAIL (password does not match)');
            process.exit(ok ? 0 : 1);
        });
        return;
    }

    let username, password, iters;
    if (first === '-p') {
        username = await readStdin('Username: ');
        password = await readStdin('Password (will echo here — run inside a closed terminal): ');
        iters = parseInt(args[1] || String(ITERATIONS_DEFAULT), 10);
    } else {
        username = first;
        password = args[1];
        iters = parseInt(args[2] || String(ITERATIONS_DEFAULT), 10);
        if (!password) { usage(); process.exit(2); }
    }

    const { formatted, secret } = await generate(username, password, iters);

    console.log('\n复制下面三行到 Cloudflare Pages → Environment variables (Production):\n');
    console.log(`ADMIN_USERNAME         = ${username}`);
    console.log(`ADMIN_PASSWORD_HASH    = ${formatted}`);
    console.log(`ADMIN_SECRET           = ${secret}`);
    console.log('\n设置完成后,请重新部署 Pages(Functions 需要在部署时加载 env vars)。\n');
}

main(process.argv).catch((e) => {
    console.error('[error]', e && e.message ? e.message : e);
    process.exit(1);
});
