// Đoạn mã gắn thanh định danh phiên kiểm thử (Email sinh viên + Trình duyệt + Độ phân giải)
// Dán vào DevTools Console trước khi chụp Screenshot bằng chứng cho Task 1 và Task 3
(() => {
  const existing = document.getElementById('qa-evidence-watermark');
  if (existing) existing.remove();
  const badge = document.createElement('div');
  badge.id = 'qa-evidence-watermark';
  const ua = navigator.userAgent;
  const browser = ua.includes('Firefox')
    ? 'Mozilla Firefox'
    : ua.includes('Safari') && !ua.includes('Chrome')
      ? 'Apple Safari'
      : 'Google Chrome';
  const updateText = () => {
    badge.innerText = `Tester: 23120268@student.hcmus.edu.vn | ${browser} (${navigator.platform}) | Viewport: ${window.innerWidth}x${window.innerHeight}`;
  };
  updateText();
  badge.style.cssText =
    'position:fixed;top:10px;right:16px;z-index:999999;background:#0f172a;color:#38bdf8;padding:6px 14px;border-radius:6px;font-family:monospace;font-size:12px;font-weight:bold;border:1px solid #38bdf8;box-shadow:0 2px 10px rgba(0,0,0,0.35);pointer-events:none;';
  document.body.appendChild(badge);
  window.addEventListener('resize', updateText);
})();
