# Supabase setup

The app is configured for `hlhqeauhnkthdoapnqdz` and the public site at https://alekswithk.github.io/aca-practice/.
The publishable key in `supabase-config.mjs` is intended for browser use. Keep database passwords and secret/service-role keys out of this repository.

## Finish in the dashboard

1. Open the project's [SQL Editor](https://supabase.com/dashboard/project/hlhqeauhnkthdoapnqdz/sql/new), paste all of `supabase/schema.sql`, and run it. It creates the progress table, private read policy and version-checked save function. Running it again preserves saved progress.
2. Under **Authentication → URL Configuration**, set **Site URL** to `https://alekswithk.github.io/aca-practice/`. Add that exact URL to **Redirect URLs**. For local testing, also add `http://127.0.0.1:8011/`.
3. Create a Web application OAuth client in [Google Auth Platform](https://console.cloud.google.com/auth/overview). Use `ACA Study` as the app name and External as the audience. Set the JavaScript origin to `https://alekswithk.github.io` and the authorized redirect URI to `https://hlhqeauhnkthdoapnqdz.supabase.co/auth/v1/callback`. Request only the standard identity scopes, `openid`, email and profile.
4. In Supabase **Authentication → Sign In / Providers → Google**, enable Google and enter the Google client ID and secret. Keep the secret in Supabase, outside this repository. Add your email as a test user in Google's Audience settings while testing; switch to In production for public access. Google login does not require SMTP. See [Supabase's Google setup guide](https://supabase.com/docs/guides/auth/social-sign-in/auth-google).
5. Publish the changed static files to the site's GitHub Pages source. Include `cloud.mjs` and `supabase-config.mjs` alongside `app.js`; no build or app server is needed.

## Verify before inviting users

Run `supabase/check.sql` in the SQL Editor after the schema. It rolls back its test users and progress. It checks anonymous denial, account isolation, revision conflicts and invalid payload rejection.

Open **Account & sync** and choose **Continue with Google**. Confirm that the panel shows your email and **Saved to your account**. Start a session, answer a question and add a note. Sign in on a second browser/device and check the history and note. Sign in as a different user and confirm that the first user's answers are absent.

To move existing guest progress into your account, choose **Add this browser's guest progress** after signing in. This keeps the original guest copy. A new account does not automatically receive data from the browser's guest profile.

## Saving behavior

The browser saves immediately; cloud saves wait about a second after edits. Sync also runs when the window regains focus, the connection returns, or the page becomes hidden. **Sync now** retries a failed save. Closing a tab before a cloud request finishes can leave recent progress only in that browser until the account is opened there again.

Each account has its own browser storage key. Signing out returns to guest progress. Account copies remain in that browser for recovery, so use a private browser session on a shared computer. Export JSON remains available for backups.

Cloud sync keeps distinct attempts and the newest timestamped draft per question. Version checks retry a merge when another device writes concurrently. Simultaneous edits to the same draft use the device timestamps; keep device clocks accurate. Conflicting attempt IDs stop sync without overwriting either copy.

An existing device keeps its current session and preferences. A device with no cached account progress restores these from the cloud. Use one device at a time for an active exam. Reset applies to guest data only and is disabled while signed in. Account-wide history deletion and live updates between devices are not included.

## Local checks

```sh
node tests/core.test.mjs
node tests/cloud.test.mjs
node tests/cloud-browser.test.mjs
```

The browser check uses the same Playwright installation and environment variables as the other browser tests. It mocks Supabase and writes no real progress. Live Google authorization and database permissions need the dashboard checks above.
