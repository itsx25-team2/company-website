# Team 2 - arbetssammanfattning 2026-09-24

## Omfattning

Dagens del av Workshop 3.5-4 flyttade `company-website` från direkt bindning
till värdport 80 till hostbaserad routing genom Kubernetes Ingress. Arbetet
förberedde även spårbara och signerade container-images.

## Utgångsläge

- `company-website` körde i K3s med `hostPort: 80`.
- Kubernetes Service var av typen `ClusterIP` på port `7000`.
- Helm och en Ingress-controller saknades.
- Pipelinen publicerade endast taggen `latest`.
- Cosign-signering och policy-controller saknades.

## Helm och ingress-nginx

Helm installerades på `team2-primary` från den signerade paketkällan efter att
paketnyckelns fingerprint hade verifierats. Installerad version blev Helm
`v4.3.0`.

`ingress-nginx` installerades därefter i namespace `ingress-nginx`:

- chart: `ingress-nginx-4.15.1`
- app-version: `1.15.1`
- extern internadress: `10.0.2.3`
- slutlig Helm-status: `deployed`, revision 2

## Portkonflikt och lösning

När K3s LoadBalancer tog över port 80 kunde den befintliga webbpodden inte
schemaläggas. Scheduler-eventet visade att noden saknade en ledig efterfrågad
värdport.

`hostPort: 80` togs först bort från den aktiva deploymenten för att återställa
appen och därefter permanent från `k8s/deployment.yaml`. Webbpodden och
Ingress-controllern återgick till `Running`.

## Kubernetes och pipeline

Följande förändringar förbereddes och validerades:

- `k8s/ingress.yaml` routar `company-website.team2.arpa` till Service-port
  `7000`.
- GitHub-deployerns RBAC omfattar `networking.k8s.io/ingresses`.
- RBAC-filen bootstrapades manuellt och `create`, `patch` samt `delete`
  verifierades med `kubectl auth can-i`.
- Deploymenten får labeln `git.commit` från aktuell GitHub-SHA.
- Pipelinen applicerar Ingress tillsammans med övriga manifest.
- Manifesten godkändes med Kubernetes server-side dry-run.

## Image-spårbarhet

Workflowen har förberetts för att:

- använda `actions/checkout@v5` och `docker/login-action@v4`,
- skapa metadata med `docker/metadata-action@v6`,
- publicera både `latest` och en kort commit-SHA-tagg,
- bygga med `docker/build-push-action@v7`,
- deploya imagen med dess oföränderliga digest.

## Cosign

Workflowen har även förberetts för nyckellös Cosign-signering:

- jobbet får `id-token: write` för GitHub OIDC,
- `sigstore/cosign-installer@v4.1.0` installerar Cosign `v2.6.4`,
- exakt den digest som byggs och deployas signeras.

Sigstores policy-controller installerades i namespace `cosign-system`:

- chart: `policy-controller-0.10.8`
- app-version: `0.13.1`
- Helm-status: `deployed`

`k8s/image-policy.yaml` begränsar den tillåtna identiteten till Team 2:s
`deploy.yml` på `main` och godkändes med server-side dry-run.

## Verifiering

Efter att Ingress hade synkroniserats verifierades:

```text
company-website.team2.arpa -> 10.0.2.3
HTTP 200 från primary med korrekt Host-header
HTTP 200 från Jonnys WSL-klient via MagicDNS
```

Ingress-controller, webbdeployment och policy-controller var `Running` vid
slutkontrollen.

## Enforcement-verifiering

- `ClusterImagePolicy` `verify-company-website` är applicerad.
- Namespace `default` har labeln `policy.sigstore.dev/include=true`.
- En server-side dry-run med osignerad `alpine:latest` nekades som förväntat.
- Team 2:s signerade image-digest godkändes i server-side dry-run.
- Den befintliga webbdeploymenten fortsatte vara `Running` och gav HTTP `200`.
- Inga credentials, tokens eller flaggvärden har lagts i Git.

## Git-status

Följande commits finns på `member/itzmejonny92`:

- `63863b3` - Ingress, RBAC och borttagning av `hostPort`.
- `6fb9751` - image-taggar, metadata och digest-baserad deployment.
- `94acaa2` - Cosign-signering och image-policy.

Ändringarna mergades till `main` via PR #16 i mergecommit `9378fc7`.
Deploy-workflowen slutfördes och den signerade digest som byggdes är samma
digest som körs i Kubernetes.

## Uppföljning

- Följ nästa deploy-workflow och bekräfta att signerade framtida digests
  godkänns av policyn.
- Uppdatera policyidentiteten kontrollerat om workflowfilens namn eller branch
  ändras.
- Rollback testades från den senaste signerade digesten `fd41c7c` till den
  tidigare signerade digesten `a8c98ac`.
- Den äldre versionen blev `Ready` och svarade med HTTP `200` via Ingress.
- Därefter återställdes deploymenten till `fd41c7c`; slutläget var `1/1` redo
  repliker och HTTP `200`.
- APP-08 kan därför markeras som `Done` efter merge av dokumentationen.
