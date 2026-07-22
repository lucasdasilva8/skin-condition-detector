(function () {
  const hostname = location.hostname;
  const isBrowserLocal =
    hostname === "localhost" || hostname === "127.0.0.1";

  const cap = window.Capacitor || window.SkinScanNative?.Capacitor;
  const isNative = Boolean(
    cap && typeof cap.isNativePlatform === "function" && cap.isNativePlatform()
  );

  const productionApi = "https://skin-condition-detector-api.onrender.com";
  const localApi = "http://localhost:8000";

  // Native apps (Simulator + device) use Render by default — a real iPhone
  // cannot reach your Mac's localhost. For Simulator + local backend, set:
  //   window.__SKINSCAN_API_URL__ = "http://localhost:8000"
  // before config.js, or create frontend/config.local.js (see APP.md).
  let apiUrl = productionApi;
  if (window.__SKINSCAN_API_URL__) {
    apiUrl = window.__SKINSCAN_API_URL__;
  } else if (!isNative && isBrowserLocal) {
    apiUrl = localApi;
  }

  window.APP_CONFIG = {
    API_URL: apiUrl,
    IS_NATIVE: isNative,
    PLATFORM: cap?.getPlatform?.() || "web",
  };
})();
