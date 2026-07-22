# SkinScan iOS app

SkinScan iPhone app wraps the existing web UI with [Capacitor](https://capacitorjs.com). Analyze still calls the FastAPI backend (Render in production).

## Requirements

- Node.js 20+
- Xcode 16+ (from the Mac App Store)
- Apple ID (Simulator works with a free account; TestFlight / device installs need the Apple Developer Program)
- For Analyze on a **physical iPhone**: backend at `https://skin-condition-detector-api.onrender.com` must be live with the ensemble models

## One-time setup

```bash
cd /path/to/skin-condition-detector
npm install
npm run build:native   # bundles Capacitor Camera into frontend/native.js
npx cap sync ios
npx cap open ios       # opens Xcode
```

In Xcode:

1. Select the **App** target → **Signing & Capabilities**
2. Choose your **Team** (personal Apple ID is fine for Simulator)
3. Pick an iPhone Simulator (e.g. iPhone 16)
4. Press **Run** (▶)

## Day-to-day workflow

After changing HTML/CSS/JS:

```bash
npm run build:native   # only if you changed scripts/native-entry.js
npx cap sync ios
# then Rebuild/Run in Xcode
```

Shortcuts:

```bash
npm run cap:sync   # sync web assets into ios/
npm run cap:open   # open Xcode
npm run cap:ios    # sync + open
```

## API URL behavior

| Environment | API |
|-------------|-----|
| Browser on `localhost:3000` | `http://localhost:8000` |
| iOS app (Simulator or device) | `https://skin-condition-detector-api.onrender.com` |

**Simulator + local backend:** create `frontend/config.local.js` (gitignored) loaded before `config.js`, or set in Safari Web Inspector:

```js
window.__SKINSCAN_API_URL__ = "http://localhost:8000";
```

Then reload. Note: a **physical phone** still cannot reach your Mac via `localhost` unless you use your Mac’s LAN IP and ATS exceptions (not covered here).

Optional local override file pattern — add before `config.js` in HTML when debugging:

```html
<script src="config.local.js"></script>
```

## Camera

On the Analyze screen inside the app you get:

- **Take photo**
- **Choose from library**

Browser builds keep drag-and-drop / file picker.

## Daily habits

- **Habits** tab: check off today’s care prompts, turn habits on/off, optional morning/evening reminder times
- **Home**: Today’s habits checklist near the top
- Phone notifications work in the Capacitor iOS app when you enable them on the Habits tab (permission prompt)
- Data is stored on-device (`localStorage`) — not sent to the server

## TestFlight (later)

1. Enroll in [Apple Developer Program](https://developer.apple.com/programs/)
2. In Xcode: **Product → Archive**
3. Distribute to TestFlight via App Store Connect
4. Keep the App Store listing clear that SkinScan is **educational / not a medical device**

## Project layout

```
capacitor.config.json   # appId com.lucasdasilva.skinscan
frontend/               # web UI (Capacitor webDir)
ios/                    # Xcode project (SPM plugins; CocoaPods not required)
scripts/native-entry.js # source for frontend/native.js
```
