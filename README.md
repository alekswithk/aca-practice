# ACA practice

A study app for ACA exam questions. Practice by topic, take timed exams, add notes, and review your history. It runs in the browser with no install.

## Open it on the web

**https://alekswithk.github.io/aca-practice/**

Sign in with Google to save progress to your account. Without signing in, progress stays in that browser.

## Run it locally

Use Python 3 and a modern browser. No build step is needed.

```sh
cd aca-practice
python3 -m http.server 8011 --bind 127.0.0.1
```

Then open **http://127.0.0.1:8011**. Opening `index.html` directly will not load the question bank.

## More

- [Content validation](CONTENT_VALIDATION.md): question counts and study clarifications.
- [Supabase setup](SUPABASE_SETUP.md): database, Google login and deployment.
- [Test report](TEST_REPORT.md): the checks that were run.
