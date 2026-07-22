/**
 * Bundled Capacitor bridge for the vanilla frontend (no Vite app).
 * Rebuild: npm run build:native
 */
import { Capacitor } from "@capacitor/core";
import { Camera, CameraResultType, CameraSource } from "@capacitor/camera";
import { StatusBar, Style } from "@capacitor/status-bar";
import { SplashScreen } from "@capacitor/splash-screen";
import { App } from "@capacitor/app";
import { LocalNotifications } from "@capacitor/local-notifications";

async function initNativeChrome() {
  if (!Capacitor.isNativePlatform()) return;
  try {
    await StatusBar.setStyle({ style: Style.Dark });
    await StatusBar.setBackgroundColor({ color: "#1b4332" });
  } catch (_) {
    /* web or unsupported */
  }
  try {
    await SplashScreen.hide();
  } catch (_) {
    /* optional */
  }
}

initNativeChrome();

window.SkinScanNative = {
  Capacitor,
  Camera,
  CameraResultType,
  CameraSource,
  StatusBar,
  SplashScreen,
  App,
  LocalNotifications,
};

// So config.js can detect native before app code runs.
window.Capacitor = Capacitor;
