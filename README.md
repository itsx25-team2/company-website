# Company Website - ITSX25 Team 2

Detta repository innehåller Team 2:s applikation och CI/CD-flöde för Kurs 6,
Workshop 3 Blue Team. Applikationen är byggd med Flask, paketeras som en
container i GitHub Container Registry (GHCR) och driftsätts automatiskt till
teamets K3s-kluster.

## Aktuell status

- GitHub-repot och GHCR-paketet är publika.
- GitHub Actions bygger och publicerar containerimagen.
- En kortlivad GitHub-runner ansluter till teamets Headscale-miljö.
- Runnern när K3s API via subnet-routen till `10.0.2.3`.
- Deployment, PersistentVolumeClaim och Service är applicerade i K3s.
- Podden är verifierad som `Running` och `/healthz` rapporterar en frisk
  applikation med databasanslutning.
- `main` skyddas med branch protection och krav på två godkännanden.
- `ingress-nginx` är installerat och routar det interna namnet
  `company-website.team2.arpa` till applikationens Service.
- Åtkomst via MagicDNS och Ingress är verifierad med HTTP-status `200`.
- Cosign-enforcement är aktivt i namespace `default`. En osignerad testimage
  nekades medan Team 2:s signerade digest godkändes.

Den tekniska setupen för Workshop 3 är klar. Defensiv analys av applikationen
har påbörjats och observationer dokumenteras utan credentials eller
flaggvärden. Åtgärdsförslag hanteras via Issues, backlog, branch och pull
request.

## Viktiga filer

- [.github/workflows/deploy.yml](.github/workflows/deploy.yml): bygger imagen,
  ansluter en tillfällig runner till Headscale och driftsätter till K3s.
- [k8s/deployment.yaml](k8s/deployment.yaml): applikationens Deployment.
- [k8s/pvc.yaml](k8s/pvc.yaml): persistent lagring för SQLite-data.
- [k8s/service.yaml](k8s/service.yaml): intern Kubernetes Service.
- [k8s/ingress.yaml](k8s/ingress.yaml): hostbaserad routing för
  `company-website.team2.arpa`.
- [k8s/github-permissions.yaml](k8s/github-permissions.yaml): RBAC för
  GitHub-deployern; appliceras manuellt som engångskonfiguration.
- [k8s/image-policy.yaml](k8s/image-policy.yaml): Cosign-policy för images
  signerade av Team 2:s deploy-workflow på `main`.
- [scripts/generate-kubeconfig.sh](scripts/generate-kubeconfig.sh): genererar
  en begränsad kubeconfig för CI/CD.
- [docs/](docs/): backlog, status, guider och gemensamma sammanfattningar.
- [members/](members/): personliga anteckningar och arbetssammanfattningar.

## Dokumentation

- [Dokumentationsöversikt](docs/README.md)
- [Produktbacklog](docs/product_backlog.md)
- [Workshop 3 - setup och verifiering](docs/workshop3_setup_status.md)
- [Teamsammanfattning 2026-09-21](docs/team_work_summary_2026-09-21.md)
- [Teamsammanfattning 2026-09-24](docs/team_work_summary_2026-09-24.md)

## Relaterad infrastruktur

Applikationens GCP-, Headscale-, nätverks- och K3s-infrastruktur hanteras i det
separata [infra-repot](https://github.com/itsx25-team2/kurs6-team2-infra).

- [Gemensam anslutningsguide](https://github.com/itsx25-team2/kurs6-team2-infra/blob/main/docs/gemensam_anslutningsguide.md)
- [Infra-repots README](https://github.com/itsx25-team2/kurs6-team2-infra/blob/main/README.md)
- [Infra-backlog](https://github.com/itsx25-team2/kurs6-team2-infra/blob/main/docs/product_backlog.md)

Normal åtkomst till privata resurser sker via personliga Tailscale-noder,
annonserade subnet-rutter och Split DNS. SOCKS5 är endast en dokumenterad
reservmetod.

## Arbetsflöde

1. Skapa eller välj ett GitHub Issue.
2. Arbeta från en egen branch, exempelvis `member/itzmejonny92` eller en kort
   feature-branch.
3. Gör en liten och tydligt avgränsad ändring.
4. Kör relevanta tester lokalt.
5. Pusha branchen och skapa en pull request mot `main`.
6. Kontrollera CI-resultatet.
7. Låt minst två medlemmar granska och godkänna.
8. Merga till `main` och verifiera deploymenten.
9. Uppdatera Issue och backlog efter verifierad merge.

Backlogfilen synkroniseras inte automatiskt med GitHub Issues. Den som ändrar
ett Issue ansvarar därför för att bedöma om även backloggen ska uppdateras.

## Lokal utveckling

Skapa en virtuell miljö och installera beroenden:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Starta applikationen:

```bash
cp .env.example .env
python wsgi.py
```

Alternativt med Flask CLI:

```bash
export PYTHONPATH=src
flask --app company_website run --port 7000
```

## Docker

```bash
docker compose up --build
```

SQLite-databasen sparas i Docker-volymen `app-data`. I K3s används i stället
en PersistentVolumeClaim monterad på `/app/data`.

## Tester

```bash
pytest
```

## Deployment

En push till `main` eller en manuell `workflow_dispatch` startar pipelinen:

1. Koden checkas ut.
2. Metadata för `latest` och aktuell commit-SHA skapas.
3. Containerimagen byggs, publiceras i GHCR och identifieras med digest.
4. Imagen signeras nyckellöst med Cosign och GitHub OIDC.
5. En kortlivad Headscale-nyckel skapas.
6. GitHub-runnern ansluter med taggen `tag:github-runner`.
7. Subnet-route och TCP 6443 till K3s verifieras.
8. Kubernetes-manifesten, inklusive Ingress, appliceras.
9. Rollout till den signerade imagen verifieras.

Workflowet använder GitHub Secrets och Variables. Hemliga värden får aldrig
skrivas i dokumentation, Issues, loggar eller commits.

## Projektstruktur

```text
.
|-- .github/workflows/
|-- docs/
|-- k8s/
|-- members/
|-- scripts/
|-- src/company_website/
|-- tests/
|-- Dockerfile
|-- docker-compose.yml
|-- requirements.txt
`-- wsgi.py
```

## Säkerhet

- Använd aldrig riktiga credentials i kod eller dokumentation.
- Kontrollera `git status` och diffen före varje commit.
- Kubeconfig och Headscale API-nyckel lagras endast som GitHub Secrets.
- Den tillfälliga CI-noden får endast den åtkomst som behövs för deployment.
- Images taggas för spårbarhet, deployas med digest och signeras nyckellöst
  med Cosign.
- Policy-enforcement aktiveras först efter verifierad signering för att
  undvika att blockera en giltig rollout.
- Kursens analys genomförs endast i de miljöer som utbildaren har godkänt.
- Flaggar dokumenteras inte öppet i gemensamma filer.
