# Workshop 3 - setup och verifiering

Datum: 2026-09-21

## Resultat

Workshopens tekniska setup är genomförd.

| Område | Status | Verifiering |
| --- | --- | --- |
| Kursrepo | Klar | Utbildarens repository är klonat och originalremote finns kvar som `instructor` |
| GitHub-organisation | Klar | `itsx25-team2` är skapad och teamet har repositoryatkomst |
| Applikationsrepo | Klar | `itsx25-team2/company-website` är publikt |
| Primary | Klar | Instansen kör `e2-small` och har verifierad internetatkomst |
| K3s | Klar | K3s är aktivt utan Traefik och metrics-server |
| Kubernetes RBAC | Klar | Begränsad `github-deployer` är applicerad |
| Kubeconfig | Klar | Begränsad kubeconfig lagras som GitHub Secret |
| Headscale CI-användare | Klar | `github-ci` finns och har en tillfällig CI-nod vid deployment |
| Headscale-policy | Klar | `tag:github-runner` får nå `10.0.2.3:6443` och ICMP |
| CI/CD | Klar | Slutlig GitHub Actions-körning är godkänd |
| GHCR | Klar | Containerpaketet är publikt |
| K3s workload | Klar | Podden är `Running`, PVC är `Bound` och health check är godkänd |

## Viktiga lärdomar

- En policyfil med läge `640` måste ha gruppen `headscale` när tjänsten kör som
  `headscale:headscale`. `root:root` hindrade policyn från att laddas.
- `tailscale/github-action@v4` lägger redan till `--accept-routes`; flaggan ska
  inte skickas en andra gång via `args`.
- En privat GHCR-image ger `ImagePullBackOff` utan registry-credential.
- En ennodsmiljö med `hostPort: 80` kan få portkonflikt vid standardiserad
  rolling update.

## GitHub Actions

Verifierad slutkörning:

- Run ID: `35597701261`
- Resultat: godkänd
- Stegen för build, Headscale, route, kubeconfig och deployment passerade.

## Kvarvarande arbete

1. Analysera applikationen i den egna godkända kursmiljön.
2. Dokumentera observationer, risker och defensiva åtgärdsförslag.
3. Genomför det godkända momentet mot den skarpa kursmiljön.
4. Gör policyinstallation, image-taggar och rolloutstrategi mer reproducerbara.

Hemliga värden och flaggvärden ska inte dokumenteras i detta repository.
