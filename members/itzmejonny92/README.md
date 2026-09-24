# Jonny Nguyen - Personlig Dokumentationsyta

Denna mapp används för Jonnys individuella anteckningar, arbetssammanfattningar
och defensiva analyser i projektet.

## Dokument i denna mapp

| Dokument | Innehåll |
| --- | --- |
| [Arbetssammanfattning 2026-09-21](work_summary_2026-09-21.md) | Individuellt arbete med applikationsrepot, K3s-driftsättning och säker dokumentation. |
| [Teamsammanfattning 2026-09-24](../../docs/team_work_summary_2026-09-24.md) | Dagens verifierade arbete med MagicDNS, Ingress, image-spårbarhet och Cosign. |

## Aktuell status 2026-09-24

- `company-website.team2.arpa` svarar med HTTP `200` via Headscale MagicDNS
  och Kubernetes Ingress.
- Ingress-, pipeline- och Cosign-ändringarna är mergade via PR #16 och den
  signerade digest som byggdes körs i Kubernetes.
- Cosign-enforcement är aktivt. En osignerad testimage nekades och Team 2:s
  signerade digest godkändes.

## Relaterad infra-dokumentation

Dokumenten nedan ligger i det separata
[`kurs6-team2-infra`](https://github.com/itsx25-team2/kurs6-team2-infra)-repot.
Gemensamma dokument länkar till `main`. Personliga dokument som ännu inte har
mergats länkar till `member/itzmejonny92`.

| Dokument | Innehåll |
| --- | --- |
| [Jonnys personliga infra-mapp](https://github.com/itsx25-team2/kurs6-team2-infra/tree/member/itzmejonny92/members/itzmejonny92) | Samlad personlig dokumentation för infra- och Blue Team-arbetet. |
| [Samlad flagganalys 2026-09-24](https://github.com/itsx25-team2/kurs6-team2-infra/blob/member/itzmejonny92/members/itzmejonny92/flaggar_individuell_sammanfattning_2026-09-24.md) | Status och pedagogisk förklaring för kursens flaggområden utan flaggvärden. |
| [Arbetssammanfattning 2026-09-22](https://github.com/itsx25-team2/kurs6-team2-infra/blob/member/itzmejonny92/members/itzmejonny92/work_summary_2026-09-22.md) | LookingGlass, Metadata Service och Cloud Storage-versionering. |
| [Personlig anslutningsguide](https://github.com/itsx25-team2/kurs6-team2-infra/blob/member/itzmejonny92/members/itzmejonny92/anslutning_via_proxy.md) | Anslutning till Spectre via SSH-tunnel, SOCKS5 och Opera GX. |
| [Infra-repots README](https://github.com/itsx25-team2/kurs6-team2-infra/blob/main/README.md) | Gemensam projektöversikt, arkitektur och arbetssätt. |
| [Product Backlog](https://github.com/itsx25-team2/kurs6-team2-infra/blob/main/docs/product_backlog.md) | Prioriteringar, status och spårbarhet för infra-arbetet. |
| [Gemensam anslutningsguide](https://github.com/itsx25-team2/kurs6-team2-infra/blob/main/docs/gemensam_anslutningsguide.md) | Teamets gemensamma instruktioner för Headscale, Tailscale, SSH och Spectre. |

## Rutin

- Namnge sammanfattningar med datum, exempelvis `work_summary_2026-09-21.md`.
- Beskriv vad som gjordes, hur det verifierades och vad som återstår.
- Dokumentera egna slutsatser och osäkerheter.
- Lägg aldrig in credentials, privata nycklar, tokens eller flaggvärden.
- Uppdatera länkarna ovan när personliga infra-dokument mergas till `main`.

