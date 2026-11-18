/**
 * SCRIPT RESET KHÓA TÀI KHOẢN (ACCOUNT LOCKOUT RESETTER)
 * 
 * Mục đích:
 * Mở khóa toàn bộ tài khoản trong cơ sở dữ liệu `backend/database.sqlite`
 * bằng cách đặt lại `login_attempts = 0` và `locked_until = NULL`.
 * 
 * Sử dụng giữa các đợt kiểm thử Stress Test nếu có tài khoản bị khóa:
 *   node scripts/reset_account_lockout.js
 */

const path = require('path');
const fs = require('fs');

const dbPath = path.resolve(__dirname, '../backend/database.sqlite');

if (!fs.existsSync(dbPath)) {
    console.error(`[LỖI] Không tìm thấy file database tại: ${dbPath}`);
    process.exit(1);
}

// Tự động tìm sqlite3 từ backend/node_modules hoặc toàn cục
let sqlite3;
try {
    sqlite3 = require('sqlite3').verbose();
} catch (e) {
    const backendSqlitePath = path.resolve(__dirname, '../backend/node_modules/sqlite3');
    sqlite3 = require(backendSqlitePath).verbose();
}

const db = new sqlite3.Database(dbPath, (err) => {
    if (err) {
        console.error('[LỖI] Không thể kết nối cơ sở dữ liệu:', err.message);
        process.exit(1);
    }
});

db.serialize(() => {
    db.run("UPDATE users SET login_attempts = 0, locked_until = NULL", function(err) {
        if (err) {
            console.error('[LỖI] Reset tài khoản thất bại:', err.message);
        } else {
            console.log(`[THÀNH CÔNG] Đã mở khóa và reset login_attempts cho ${this.changes} tài khoản người dùng.`);
        }
        db.close();
    });
});
