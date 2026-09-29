# Individuell arbetssammanfattning - Jonny Nguyen - 2026-09-28

## Fokus

Jag arbetade med Workshop 4 i `company-website`. Målet var att integrera
utbildarens version, förstå SBOM-flödet och förbättra säkerheten utan att
påverka `main` före gruppens granskning.

## Arbetsprocess

Jag synkade repot, granskade utbildarens commits och integrerade dem på
`workshop4/instructor-sync`. Konflikter löstes manuellt så att Team 2:s
Headscale-, WIF-, RBAC-, Ingress- och deploymentlösning behölls.

Jag granskade sedan autentisering, sessionshantering, profilbehörigheter,
e-postförhandsvisning, dependencies, containerimage och CI/CD.

## Säkerhetsförbättringar

- parametriserad SQL och korrekt hashverifiering,
- säker variabelersättning för e-postsignaturer,
- CSRF-skydd och POST-baserad logout,
- ägarkontroll för profilredigering och interna anteckningar,
- blockering av avstängda användares gamla sessioner,
- extern Flask `SECRET_KEY` och säkrare sessionscookies,
- uppdaterade Python-beroenden,
- minskad runtime-image utan `pip`.

## Vad jag lärde mig om SECRET_KEY

Flasks `SECRET_KEY` är inte en GCP Service Account Key. WIF ersätter
långlivade GCP-nycklar, medan Flask fortfarande behöver en separat nyckel
för att signera sessioner och CSRF-token.

På `team2-primary` verifierade jag administrativ Kubernetes-behörighet:

```text
sudo k3s kubectl auth can-i create secrets -n default
yes
```

`company-website-secrets` skapades och kontrollerades utan att nyckelvärdet
visades eller dokumenterades.

## SBOM pedagogiskt

1. GitHub Actions bygger imagen.
2. Imagen identifieras med en oföränderlig digest.
3. Anchore skapar en CycloneDX-SBOM från exakt denna digest.
4. Cosign binder SBOM-attesteringen till samma image.
5. Cosign signerar imagen med GitHub OIDC.
6. Kubernetes deployar samma analyserade och signerade digest.

Signaturen visar vem som byggde imagen. Attesteringen visar vilket innehåll
som hör till just den imagen.

## Verifiering

- 19 tester passerade.
- `pip check` och `pip-audit` var gröna.
- Bandit rapporterade inga kodfynd.
- Docker-build och `/healthz` fungerade.
- Start utan `SECRET_KEY` stoppades som avsett.
- CycloneDX 1.5 innehöll 139 komponenter.
- Docker Scout hade två kvarvarande basimagefynd utan fixversion.
- GitHub `Application Checks` lyckades på 18 sekunder.

## Merge, felsökning och deployment

PR #21 godkändes och mergades som `3eeb631`. Den första deploymenten nådde
hela vägen genom test, image-build, SBOM, attestering och signering men
stoppades när en Headscale-engångsnyckel skulle skapas.

Jag spårade felet till att den lagrade Headscale API-nyckeln hade löpt ut.
Detta är inte en GCP Service Account Key: WIF och Cosign fortsätter att vara
nyckellösa via GitHub OIDC. Headscale API-nyckeln är i stället den
tidsbegränsade kontrollcredential som får skapa en automatisk engångsnyckel
för runnerns nätanslutning.

API-nyckeln roterades med 30 dagars giltighet och överfördes direkt till
GitHub Secrets utan att värdet visades eller sparades. Omkörning 2 av
deployment `36435042346` blev helt grön.

Efteråt verifierade jag:

- `1/1` redo Kubernetes-repliker och slutförd rollout,
- digestlåst image `sha256:469d57e...`,
- HTTP `200` och frisk databas via `/healthz`,
- säkra cookieflaggor,
- giltig Cosign-signatur från rätt workflow och commit,
- giltig CycloneDX-attestering för samma image-digest.

## Spårbarhet

- Branch: `workshop4/instructor-sync`
- Säkerhetshärdning: `47eb0bb`
- Action-uppdatering: `d237f53`
- [Godkänd branchkontroll](https://github.com/itsx25-team2/company-website/actions/runs/36404525054)
- [Godkänd deployment](https://github.com/itsx25-team2/company-website/actions/runs/36435042346)
- [Gemensam sammanfattning](../../docs/team_work_summary_2026-09-28.md)

## AI-användning

Jag använde OpenAI Codex för pedagogiska förklaringar, kodgranskning,
säkerhetsförslag och teststöd. Jag godkände arbetsstegen och kontrollerade
resultaten mot kursinstruktionen, repot, Pytest, Docker, `pip-audit`, Bandit
och GitHub Actions. Inget mergades automatiskt till `main`.

## Kvar att göra

- få rotationsguiden granskad och mergad,
- följa upp Tailscale Actions authkey-varning och Ubuntu 26-migrering,
- rotera Headscale API-nyckeln innan nästa utgångsdatum,
- följa upp basimagefynd när fixversioner finns.
