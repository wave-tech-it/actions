# WaveTech GitHub Actions condivise

Azioni riusabili per tutti i repo dell'org `wave-tech-it`.

## send-deploy-email

Invia email riepilogativa esito deploy (SMTP SSL Aruba, solo stdlib Python).

### Setup una tantum per repo

1. Impostare il secret `SMTP_PASSWORD` (password di `info@wavetech.it`):
   `gh secret set SMTP_PASSWORD --repo wave-tech-it/<repo>`
   oppure via web: repo → Settings → Secrets and variables → Actions → New repository secret.
   (In alternativa: secret di organizzazione `SMTP_PASSWORD` condiviso.)

2. Aggiungere il job `notify` al workflow deploy:

```yaml
notify:
  runs-on: arc-runner-set
  needs: [test, build-push, rollout]  # adattare ai job esistenti
  if: always()
  steps:
    - name: Email esito deploy
      uses: wave-tech-it/actions/send-deploy-email@v1
      with:
        password: ${{ secrets.SMTP_PASSWORD }}
        status: ${{ (contains(needs.*.result, 'failure') || contains(needs.*.result, 'cancelled')) && 'failure' || 'success' }}
        tag: ${{ needs.build-push.outputs.tag }}
```

### Input (tutti opzionali tranne `password` e `status`)

| input      | default              |
|------------|----------------------|
| `to`       | olivieri88@gmail.com |
| `smtp-host`| smtps.aruba.it       |
| `smtp-port`| 465                  |
| `username` | info@wavetech.it     |
| `from`     | info@wavetech.it     |
| `tag`      | ""                   |
