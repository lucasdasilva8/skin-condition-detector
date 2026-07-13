(function () {
  const isLocal =
    location.hostname === "localhost" || location.hostname === "127.0.0.1";

  window.APP_CONFIG = {
    API_URL: isLocal
      ? "http://localhost:8000"
      : "https://skin-condition-detector-api.onrender.com",
  };
})();
