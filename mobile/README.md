# Primer Citizen Shield — mobile app

Expo / React Native client for the citizen-facing features: note scanning, QR
scanning, number checks, call screening, the AI assistant, and the panic button.

## ⚠️ Read this before running on a phone

**`http://localhost:8000` does not work on a physical device.** The default in
[`constants/api.ts`](constants/api.ts) is fine for a simulator, but on a real phone
`localhost` is *the phone itself* — every request fails with a connection error and
the app hangs on its splash screen with "Could not reach the Primer backend".

Point it at your machine's LAN address instead:

```bash
cp .env.example .env
# then edit .env:
EXPO_PUBLIC_API_URL=http://192.168.1.42:8000   # your machine's LAN IP, not localhost
```

Find your IP with `ipconfig` (Windows) or `ifconfig | grep inet` (macOS/Linux). The
phone and the computer must be on the same network, and the backend must be listening
on all interfaces — `--host 0.0.0.0`, which the documented uvicorn command already does.

`EXPO_PUBLIC_`-prefixed variables are inlined at build time, so **restart the Expo dev
server after changing `.env`.** A stale bundle keeps the old URL and looks identical.

## Running

```bash
npm install
npx expo start          # then press i / a, or scan the QR with Expo Go
```

The backend must be up first — see [`../backend_api_contract.md`](../backend_api_contract.md).
There is no login screen: the app signs in as the seeded demo citizen
(`sumanth@primer.demo`) on launch, per the task sheet.

## Permissions

- **Camera** — note and QR scanning.
- **Location** — attached to a panic alert so responders know where it came from.
  Denying it does not block the SOS; the alert still sends, without coordinates.

## Troubleshooting

| Symptom | Cause |
| --- | --- |
| Stuck on splash, "Could not reach the Primer backend" | `EXPO_PUBLIC_API_URL` still `localhost` on a physical device, or the backend isn't running |
| Worked yesterday, now every request 401s | Expired token. The client clears it and re-authenticates automatically; if it persists, the backend's `JWT_SECRET_KEY` changed |
| `.env` edit had no effect | Expo inlines `EXPO_PUBLIC_*` at build time — restart the dev server |
| Blank map / no location on a panic alert | Location permission denied; the SOS is still delivered |
