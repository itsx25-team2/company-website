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

## Spårbarhet

- Branch: `workshop4/instructor-sync`
- Säkerhetshärdning: `47eb0bb`
- Action-uppdatering: `d237f53`
- [Godkänd branchkontroll](https://github.com/itsx25-team2/company-website/actions/runs/36404525054)
- [Gemensam sammanfattning](../../docs/team_work_summary_2026-09-28.md)

## AI-användning

Jag använde OpenAI Codex för pedagogiska förklaringar, kodgranskning,
säkerhetsförslag och teststöd. Jag godkände arbetsstegen och kontrollerade
resultaten mot kursinstruktionen, repot, Pytest, Docker, `pip-audit`, Bandit
och GitHub Actions. Inget mergades automatiskt till `main`.

## Kvar att göra

- skapa PR och invänta minst två godkännanden,
- verifiera deployment från `main`,
- verifiera publicerad SBOM-attestering och Cosign-signatur,
- följa upp basimagefynd när fixversioner finns.
