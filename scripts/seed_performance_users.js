/**
 * SCRIPT SEED VÀ ĐỒNG BỘ DỮ LIỆU TÀI KHOẢN KIỂM THỬ HIỆU NĂNG
 * File: scripts/seed_performance_users.js
 * 
 * Mục đích:
 * 1. Nạp và đồng bộ 500 tài khoản người dùng từ `data/users.csv` vào `backend/database.sqlite`.
 * 2. Đảm bảo 100% mật khẩu trùng khớp với CSV, reset `login_attempts = 0` và `locked_until = NULL`.
 * 3. Tự động kiểm tra trực tiếp qua HTTP API đến backend `http://localhost:3000/api/login` để xác minh.
 * 
 * LƯU Ý SỐNG CÒN VỀ KIẾN TRÚC ESHOP:
 * - Trong mã nguồn `backend/database.js` của hệ thống EShop, hàm `initDatabase()` được gọi
 *   vô điều kiện mỗi khi tiến trình `node server.js` khởi động lại.
 * - Khi đó, server sẽ thực hiện `DROP TABLE IF EXISTS users` và chỉ nạp 2 user mặc định (admin & test).
 * - DO ĐÓ: Bất cứ khi nào bạn khởi động lại backend (`node server.js`), bạn PHẢI CHẠY LẠI script này
 *   ngay sau khi server đã bật (trong khi server đang chạy) để nạp lại 500 tài khoản trước khi chạy JMeter!
 */

const fs = require('fs');
const path = require('path');
const http = require('http');

// Tự động tìm sqlite3 từ backend/node_modules hoặc toàn cục
let sqlite3;
try {
    sqlite3 = require('sqlite3').verbose();
} catch (e) {
    const backendSqlitePath = path.resolve(__dirname, '../backend/node_modules/sqlite3');
    try {
        sqlite3 = require(backendSqlitePath).verbose();
    } catch (e2) {
        console.error('[LỖI] Không tìm thấy thư viện sqlite3. Hãy đảm bảo đã cài đặt trong thư mục backend.');
        process.exit(1);
    }
}

// Định vị đường dẫn file database và CSV độc lập với thư mục thực thi lệnh (CWD)
const rootDir = path.resolve(__dirname, '..');
const dbPath = path.resolve(rootDir, 'backend/database.sqlite');
const csvPath = path.resolve(rootDir, 'data/users.csv');

console.log('================================================================');
console.log('       ESHOP PERFORMANCE USERS SEEDER & VERIFICATION            ');
console.log('================================================================');
console.log(`[ĐƯỜNG DẪN] Thư mục gốc: ${rootDir}`);
console.log(`[ĐƯỜNG DẪN] Database:   ${dbPath}`);
console.log(`[ĐƯỜNG DẪN] Users CSV:  ${csvPath}`);

if (!fs.existsSync(dbPath)) {
    console.error(`[LỖI] Không tìm thấy file database tại: ${dbPath}`);
    console.error('      Vui lòng khởi động backend ít nhất 1 lần (cd backend && node server.js) để tạo DB.');
    process.exit(1);
}

if (!fs.existsSync(csvPath)) {
    console.error(`[LỖI] Không tìm thấy file CSV tại: ${csvPath}`);
    process.exit(1);
}

const db = new sqlite3.Database(dbPath, (err) => {
    if (err) {
        console.error('[LỖI] Không thể kết nối tới cơ sở dữ liệu SQLite:', err.message);
        process.exit(1);
    }
});

// Helper promises cho db
function run(sql, params = []) {
    return new Promise((resolve, reject) => {
        db.run(sql, params, function(err) {
            if (err) reject(err);
            else resolve(this);
        });
    });
}

function get(sql, params = []) {
    return new Promise((resolve, reject) => {
        db.get(sql, params, (err, row) => {
            if (err) reject(err);
            else resolve(row);
        });
    });
}

async function main() {
    // Đọc và phân tích file CSV (hỗ trợ cả Windows CRLF và Linux LF)
    const fileContent = fs.readFileSync(csvPath, 'utf-8');
    const lines = fileContent.split(/\r?\n/).map(l => l.trim()).filter(l => l.length > 0);
    const header = lines[0];
    const dataRows = lines.slice(1);

    console.log(`[BƯỚC 1/4] Đã đọc thành công ${dataRows.length} dòng tài khoản từ file CSV.`);

    await run("BEGIN TRANSACTION");

    let insertedCount = 0;
    let updatedCount = 0;

    for (const line of dataRows) {
        // Parse CSV an toàn hỗ trợ chuỗi có dấu ngoặc kép
        const parts = line.match(/(".*?"|[^",]+)(?=\s*,|\s*$)/g) || [];
        const cleanParts = parts.map(p => p.replace(/^"|"$/g, '').trim()).filter(p => p !== '');

        if (cleanParts.length >= 5) {
            const [email, password, name, phone, address] = cleanParts;

            const existing = await get("SELECT id FROM users WHERE email = ?", [email]);
            if (existing) {
                // Đã tồn tại -> Cập nhật lại mật khẩu chuẩn và mở khóa
                await run(
                    `UPDATE users 
                     SET name = ?, password = ?, phone = ?, shipping_address = ?, login_attempts = 0, locked_until = NULL 
                     WHERE email = ?`,
                    [name, password, phone, address, email]
                );
                updatedCount++;
            } else {
                // Chưa tồn tại -> Chèn mới
                await run(
                    `INSERT INTO users (name, email, password, role, phone, shipping_address, login_attempts, locked_until)
                     VALUES (?, ?, ?, 'user', ?, ?, 0, NULL)`,
                    [name, email, password, phone, address]
                );
                insertedCount++;
            }
        }
    }

    await run("COMMIT");
    console.log(`[BƯỚC 2/4] Đồng bộ dữ liệu hoàn tất! (Chèn mới: ${insertedCount}, Cập nhật: ${updatedCount})`);

    // Kiểm tra số lượng trong Database
    const rowTotal = await get("SELECT COUNT(*) as total FROM users");
    const rowPerf = await get("SELECT COUNT(*) as perfTotal FROM users WHERE email LIKE 'perf_user%'");
    const total = rowTotal ? rowTotal.total : 0;
    const perfTotal = rowPerf ? rowPerf.perfTotal : 0;

    console.log(`[BƯỚC 3/4] Thống kê Database hiện tại:`);
    console.log(`           - Tổng số tài khoản trong DB:       ${total}`);
    console.log(`           - Tài khoản kiểm thử (perf_user_*): ${perfTotal}`);

    db.close();

    // Bước 4: Kiểm tra trực tiếp API nếu server đang chạy
    verifyServerLogin();
}

function verifyServerLogin() {
    console.log(`[BƯỚC 4/4] Kiểm tra trực tiếp xác thực với Backend API (http://localhost:3000)...`);
    
    const postData = JSON.stringify({
        email: 'perf_user_001@eshop.com',
        password: 'Test1234!'
    });

    const options = {
        hostname: 'localhost',
        port: 3000,
        path: '/api/login',
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Content-Length': Buffer.byteLength(postData)
        },
        timeout: 2000
    };

    const req = http.request(options, (res) => {
        let body = '';
        res.on('data', (chunk) => body += chunk);
        res.on('end', () => {
            if (res.statusCode === 200) {
                console.log(`[THÀNH CÔNG TUYỆT ĐỐI] HTTP 200 OK! API Login chấp nhận tài khoản perf_user_001@eshop.com.`);
                console.log(`                      Token JWT đã được sinh hợp lệ.`);
                console.log('----------------------------------------------------------------');
                console.log('=> HỆ THỐNG ĐÃ HOÀN TOÀN SẴN SÀNG ĐỂ CHẠY LOAD/STRESS/SPIKE TEST!');
                console.log('================================================================');
            } else {
                console.error(`[CẢNH BÁO] API trả về HTTP ${res.statusCode}: ${body}`);
            }
        });
    });

    req.on('error', (e) => {
        console.log(`[CHÚ Ý] Backend server hiện chưa bật trên port 3000 (${e.message}).`);
        console.log(`        Hãy đảm bảo chạy 'cd backend && node server.js' trước khi chạy JMeter.`);
        console.log(`        QUAN TRỌNG: Nếu server vừa khởi động lại, hãy chạy lại script này một lần nữa!`);
        console.log('================================================================');
    });

    req.on('timeout', () => {
        req.destroy();
        console.log(`[CHÚ Ý] Timeout khi kết nối tới localhost:3000.`);
    });

    req.write(postData);
    req.end();
}

main().catch((err) => {
    console.error('[LỖI KHÔNG MONG MUỐN]:', err);
    process.exit(1);
});
