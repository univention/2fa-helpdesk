# Changelog

## [0.5.1](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/compare/v0.5.0...v0.5.1) (2025-06-25)


### Bug Fixes

* fix ingress template, and change path to `univention/2fa/ui` ([dbd49df](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/dbd49dffa701e863da90757681606f5e2143bd04)), closes [univention/dev/internal/team-nubus#1239](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1239)

## [0.5.0](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/compare/v0.4.1...v0.5.0) (2025-06-23)


### Features

* refactor secret handling for keycloak secrets ([73a8b4d](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/73a8b4dd5a79da152a943bf4780184e3c1b72332)), closes [univention/dev/internal/team-nubus#1219](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1219)


### Bug Fixes

* use default cluster ingress class if not defined ([f4f784f](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/f4f784f4a4c5ff0fb139a5ac8e188d2f03f337bd)), closes [univention/dev/internal/team-nubus#1134](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1134)

## [0.4.1](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/compare/v0.4.0...v0.4.1) (2025-06-23)


### Bug Fixes

* bump umc-base-image version ([2ac2070](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/2ac2070f13bc1e3a8bc5c7761510803a65b543ea)), closes [univention/dev/internal/team-nubus#1263](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1263)

## [0.4.0](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/compare/v0.3.5...v0.4.0) (2025-06-13)


### Features

* refactor provisioning to follow Nubus style ([fa4e589](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/fa4e589b7b4f72690e21f3836cf03f44116dd5df)), closes [univention/dev/internal/team-nubus#1213](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1213)


### Bug Fixes

* QA suggestions ([06b90fc](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/06b90fc08a362134bdc12fcc1f551cbece6f0d0c)), closes [univention/dev/internal/team-nubus#1213](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1213)

## [0.3.5](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/compare/v0.3.4...v0.3.5) (2025-06-11)


### Bug Fixes

* **twofa-frontend:** use univention nginx image ([565722f](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/565722f4098c9b1f1a2f08679e49d274c08d559e)), closes [univention/dev/internal/team-nubus#1224](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1224)

## [0.3.4](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/compare/v0.3.3...v0.3.4) (2025-06-11)


### Bug Fixes

* resolved linter issue on extension's README ([73614d7](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/73614d784541f3c84983c858076c7c1c165fe196)), closes [univention/dev/internal/team-nubus#1214](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1214)

## [0.3.3](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/compare/v0.3.2...v0.3.3) (2025-06-10)


### Bug Fixes

* allow deactivate tiles from data-loader ([fb9d862](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/fb9d8625e795f142599f9f88cb63fc7afb42c6ab)), closes [univention/dev/internal/team-nubus#1211](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1211)

## [0.3.2](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/compare/v0.3.1...v0.3.2) (2025-06-06)


### Bug Fixes

* remove old file ([e769889](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/e769889a75fffe0c1cf7a63b81e6dab70fbdf97c))

## [0.3.1](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/compare/v0.3.0...v0.3.1) (2025-06-06)


### Bug Fixes

* change extension to use ucs-base-image, remove useless folders, restructure plugins folder ([9600097](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/9600097aa549bca748c18b6d15b260dbdea22434))

## [0.3.0](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/compare/v0.2.1...v0.3.0) (2025-06-05)


### Features

* all containers run as non-root w/ read-only file systems ([0942b44](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/0942b44ee6b35c7c63c4538264ef605931f7bde3)), closes [univention/dev/internal/team-nubus#1212](https://git.knut.univention.de/univention/dev/internal/team-nubus/issues/1212)

## [0.2.1](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/compare/v0.2.0...v0.2.1) (2025-06-03)


### Bug Fixes

* add stub values for error error message ([4326bb9](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/4326bb9fa22b5950e13d29065222199df2fd584f))
* **helm:** set default group to match 2fa-users scheme ([c625716](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/c625716ac2b40a18521a85dd8fa53718c9854bbf))
* **helm:** template allowedGroups as jinja-loop ([b729f9c](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/b729f9cae888b2fdb3efd13e85fbb20a4bb303f2))
* **helm:** use oidc_host for frontend env ([02f43bd](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/02f43bdd20ca0f9728ffd8623e0d6cc8e01323ba))
* **helm:** user sub mapper instead of usid ([0d27e28](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/0d27e28141654dfdd5bfdce0265db2e4ce5a3e69))
* use new uid/sub mapper struct ([bff8ae9](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/bff8ae9f58ea59a48c43efdca9bc78aa7049bb55))

## [0.2.0](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/compare/v0.1.0...v0.2.0) (2025-05-25)


### Features

* templatable extension entry category ([e5fdbeb](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/e5fdbebadb8c7b55c71c29610dd0372688ac4550))


### Bug Fixes

* add self server to portalUserLinks ([3cae630](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/3cae630ee856a7cf9e1c7150dcf77b733aef8546))
* better error & payload handling ([6befd40](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/6befd40216046c23c6e29c703fd392da2adb4579))
* explicitly set https & remove path ([a4a9093](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/a4a909345df80537e69b6b934ac7b9133793c3d5))
* **helm:** remove duplicated KEYCLOAK_URL ([8ae72dc](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/8ae72dceab1576e3c7fc3be03a5543861f9f47f9))
* **helm:** use full provisoning env for init container ([c6d1497](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/c6d14979623daebdfa08578ad147517876c1f6cf))
* **helm:** use OIDC_REALM for check ([e61c459](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/e61c4599b85e78e0f3e052c6a9e94415de1360cb))
* **helm:** use realm from config map in request ([dfa73a9](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/dfa73a9a707b104632a03ed45af5b268fe14d204))
* re-enable checksum for provisioning ([9b54bb1](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/9b54bb1cc367de2b7ae7e2fcef551a9c90940050))
* re-enable portal links with new cn ([d1929bf](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/d1929bfa97cd362572a059adf4c27f9ba788fd66))
* remove debugging token ([b0f3989](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/b0f39890a29ca22d402a1b8d4984ce23fb6351c8))
* remove duplicated : ([58fbb64](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/58fbb64f3e81d8ce62a981a50f01c1ed57a1d2ca))
* remove univentionNewPortalUserLinks extension ([7a79d5b](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/7a79d5b43b7c35d3b18b4b1309351a321f7a5128))
* set position to dn & userLinks ([25a9931](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/25a9931b63b2e02a7643e5f100047ca313cb3f74))
* **values-helm:** rename default display group ([a231d66](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/a231d663fd7787225c0ddf9b16abd4f172a00308))
* **values:** use full group path by default ([07be23a](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/07be23a471bb789a51eae0467946d72127cdb09d))

## [0.1.0](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/compare/v0.0.1...v0.1.0) (2025-05-19)


### Features

* add keycloak provisioning in-chart ([0c99e11](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/0c99e115983b8b5f89efd16cb74ad97d971976ff))
* autogenerate config.json with env ([376d2e4](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/376d2e42b226a569b377de5d191c14e0e8cf9a7f))
* cleanup for self-service and general ([29f9ab8](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/29f9ab84317431e372feed50c0decfbebcfdd378))
* enable token retrival in frontend ([f3f47d0](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/f3f47d059a02e0ead890936a379964b5e228f310))
* full client scope provisioning ([244274e](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/244274e216dba129f9531ce0fa540195ee3b4646))
* integrate Keycloak for authentication and add route guards ([2e7730b](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/2e7730b36d803fc7623dc599981d14d2d86a2fe7))
* integrate Keycloak for authentication and add route guards ([7153640](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/7153640995e8f03ba2fc93f056829a8fb5c3f4c0))
* make keycloak work for admin ([e3b2114](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/e3b2114a413c6624fe96e099a5cd7116c2f68069))
* refactor and structure code so that is fetches and uses config ([4a50b77](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/4a50b7747a7f35196451b8f4b6748db2f5ca4d5e))


### Bug Fixes

* add actual token in fetches ([dbc7eb5](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/dbc7eb5f8c48247ddefd11be758e7a73c542a364))
* add loading icon ([8bb2366](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/8bb23666d659bdbed3b477c0237dfb21e9ceb2e3))
* add missing line escape ([707902a](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/707902adb7e94e5cf7b1fbb8a0314dde28c43ef2))
* admin interface description ([9e66515](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/9e665159c939bd554c917d86fd8273446633a7be))
* change backend & service to portal ([d2010d7](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/d2010d7c5150f334e21268f5227fc2c071408e83))
* change ingress service account target template ([b28cc1e](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/b28cc1e3881d57e4415e774adee8d7713a0f5587))
* change kc-provisioning to pre-upgrade ([ebed8c3](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/ebed8c3fcb0c97dac5b14cc8a2937c7704e07232))
* change to yaml-correct seperators ([637399f](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/637399fcedeecaecb487e70a461f2e4af3cd0177))
* correctly quote default fallback realm ([45e849b](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/45e849bf1694535b2519b2d1dbdd6eb3fb19e2a1))
* disable cert by default (using nubus cert) ([e3f0b1c](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/e3f0b1c803047ab67f5db2aa6194e2526755cfa1))
* double volume definition ([3c83464](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/3c83464c3a063904459edb4bd74b7e7006215df1))
* frontend token debug line ([6eb51eb](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/6eb51eb8b52edde25156a038dc13ff91d365768b))
* implement service name suffix ([6af6d77](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/6af6d774f933d47f913d0b6ee6f29848f52f784b))
* install getting stuck if dependency is not rdy ([84ff6ad](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/84ff6ad251573eece68581ed16615f4d9ae94b24))
* move admin_realm default to values ([5046110](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/5046110fea6a4f04813aa027c85ea6aae0b518e4))
* pendantic response type ([6c78823](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/6c78823769f62c79cb1ded6014dc27bee6958a01))
* reduce size ([d4e86f6](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/d4e86f6766f2d5be8adda3b15b6bf59630e75a86))
* reduce size ([ef27719](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/ef277194259c180eef74517edbfe41f40044b2e7))
* remove checksum test ([685f2b1](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/685f2b1f62ebed24c07f1f122da97936b8a9812b))
* remove comments to reduce size ([7d7229c](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/7d7229c6219af8aebc47baafdef63c4022332695))
* remove duplicated scope creation ([3ce954f](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/3ce954f4f9c0b785dbea834e746129d620b938af))
* replace old dockerfile ([695fbc3](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/695fbc32dd355ec7129015f11b3fdf57250cea0a))
* set a default value for keycloak-client name ([0d1b667](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/0d1b667b72df1b2530aab4dbb56d731666689aaa))
* set nubus url for KEYCLOAK_BASE_APP ([8d85f4f](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/8d85f4fca11727d35167c905aacd19b6f99f09ce))
* switch pages starting at 1 ([76eb688](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/76eb68852d5be777a9640c9c620161a7afcf0f54))
* template tls secretName ([dc74b6f](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/dc74b6f6861ded8189c4a96ab6fbd86dd5c4693c))
* ts issues ([9949443](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/9949443f6a60dfd66bd3501b177b633ce6c8c9fa))
* unify naming scheme further ([89de669](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/89de6693d60edf6fcc5c3f99514b9e6728ecb578))
* use correct self-service url ([40ffc16](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/40ffc16bfe2c31da9010dc10e98823cdaf405c89))
* use nubusBaseUrl ([3b77ab1](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/3b77ab1b00dc63470c15e7a38fb8c8b7b139d85e))
* use portalTwoFaLinkBase-template in links ([8f78228](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/8f78228948dd666e10e30636bbe6f0c80fb0b5a3))
* various value related improvements & fixes ([cbef1f5](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/cbef1f578c3a50feafe513cf98dca08b49cb95da))

## 0.0.1 (2025-05-13)


### Features

* add custom styles and base styles for theme customization ([addaf89](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/addaf89641ed2f533b900dde2d4e27967e6dddbf))
* add custom styles and base styles for theme customization ([b71643e](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/b71643e71d5858af07c6810b42edb46a33f52982))
* add dockerfile ([a33d573](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/a33d5735c94da6ca1cab06a487fa288bb5f425b5))
* add icon and fix input of pgaination ([00f9f18](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/00f9f18e70464086f55915f93147030e0a6db80d))
* add meta titles ([e62bdfd](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/e62bdfd0ce92a5a2fbed3f642ec1b2f89838b0fe))
* add new helm without vars ([80a8352](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/80a83521f027a8b0e99b32b7c0840f5a01972fc2))
* add placeholder probes, change internal port to 8080 WP 237 ([108ff38](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/108ff388dd3e9408a271624e69055d19751f0f7b))
* add router ([999f1bb](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/999f1bb577cbb82e4f61c984c0a57410621e1048))
* add search ([879073b](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/879073b48094ce7b1b2fb32e30609771903836b2))
* add search ([e435ef2](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/e435ef2f92006f40f7659bf52ee71f09ebad8975))
* add SelfServicePage ([77b7f69](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/77b7f69634d4aae684a7b960d829da31060c64bc))
* add styles ([3f7856f](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/3f7856f9953b9a492bc3625ce2ee7b3e4f3d7142))
* add swagger ([6756ba2](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/6756ba240f31d1f886f71195f517211a68b13222))
* add useUsers composable ([ec1e142](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/ec1e1428d85b84addc6d12f5baf039b4ba61315b))
* added headless table with simple functinality ([edc7f5c](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/edc7f5ce2fbde4c51c00f95d472bd7893d09284f))
* adjust vars in css ([e9312b9](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/e9312b99fc7e151b2e6e7a06d40ebb4e7c0a334c))
* adjust vars in css ([590aa2b](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/590aa2b053f534669f358822be3d22e15a3673e9))
* adjust vars in css ([620d0e2](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/620d0e21a6bb11df5b7abbf1eb6a3fc44b14e753))
* adjust vars in css ([38137ad](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/38137ad0b3edac4c9931a4b81aeb1ed3444de9f1))
* change config and add button ([69d68f7](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/69d68f7e94703283e39385270946c127918f095b))
* cleanup and improvements ([e00903e](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/e00903eb525e80c1c76a4f03a1b42a45224d30d5))
* cleanup and improvements ([c61cfc7](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/c61cfc70b3ed70deeacd24739b5a6501ab7e453f))
* config map creation script based on env ([172a95c](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/172a95c2951b4e2183e9d8c5319e5e14fa71d168))
* enhance button and modal components with loading states ([136c83b](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/136c83b862f954698ac80826f56e0f85ec820349))
* enhance button component and add modal for user actions ([ca473b9](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/ca473b905d68b5381456f9df336d6404b5ac3a3b))
* enhance theming with dark mode support and improve button styles ([f1406b9](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/f1406b97d80b382bee87ebb875ce1ad10ad55d46))
* enhance user overview with language support and translations ([4518f1a](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/4518f1a84f411c2a3cc8251d0bf92f139036d352))
* implement helm templates ([9ee6b3d](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/9ee6b3d6c09970f845ac5ce0e1d38ca377404f5c))
* implement language selector and translation ([acd158f](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/acd158f605a56fbab1abd1108e7295a64168324f))
* implement logout-on-reset ([e70ade6](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/e70ade63150bfcb05e008cd8c9cb812e29d2fd8e))
* implement pagination & improve queries ([9101315](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/910131545f24a11ceb9390011af36b5bc275bcf1))
* implement pagination & improve queries ([239ab3c](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/239ab3c77652d8c011d29f4707ba208b08a9e6b7))
* implement reset user token functionality and improve button transition styles ([f214766](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/f2147668732f518cfafeef15166526b590c165c7))
* improve helper scripts ([1f4a3f5](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/1f4a3f5a1cec9625d8408c878de2476296726ba6))
* initial project skeleton WP 237 ([f5ceadd](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/f5ceadd460387ccf16575ee077c13243796de48f))
* make pagination work with backend ([5115720](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/5115720ab4cf02c41b4954064703b59e72cb0165))
* make pagination work with backend ([02870db](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/02870dba44ce489348dca083a91ed56005bffce8))
* make pagination work with backend ([1e0148d](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/1e0148d3b3919b324373d8b6d0f529561dd13831))
* refactor components to use CSS variables for theming and improve accessibility ([c36a619](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/c36a619a7da08749e41e8f2f6b46f6b8cda235e0))
* remove unused vars ([f114690](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/f1146904a64cc4ea88f8ad5fedf2123479ffb8bd))
* remove unused vars ([16967bd](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/16967bd2b15e5e057f18c6bfacfe93fd5689ab9b))
* remove unused vars ([607fea7](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/607fea7d6119b8d2195c2e638cae0133529716bf))
* remove unused vars ([1e94b6a](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/1e94b6aca8132695689616507fff48f351974530))
* start work on backend ([010810d](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/010810d29f785aeeaa6159288c58499b35b57c59))
* use users from backend ([5bca57c](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/5bca57c25f5df90777deb23e48c7eb7260f44a20))


### Bug Fixes

* add explicit admin realm ([acca610](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/acca610022cd2126327eea31e2c6825cffa48bce))
* add KANIKO_BUILD_PATH & DOCKERFILE_PATH ([326fa33](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/326fa33991c488ac2f390635b1cb397269e6e8bb))
* add KANIKO_BUILD_PATH & DOCKERFILE_PATH ([e2a2bc7](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/e2a2bc71e99e151a50c398b9d2a7acc01044e5bf))
* additionally catch jwt.exceptions.DecodeError ([6b19728](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/6b197286a92b5348f8664ebf45a68648e4a8b8ee))
* backend-prefix for fastapi ([fa48b87](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/fa48b877df9abc8bacc86dfc4a87b1044ecde68d))
* container target paths ([2d0c000](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/2d0c000e75223a07ee41a8240712b0158d0cf8ea))
* correctly use openapi-valid datastructures everywhere ([4b41b57](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/4b41b576ae4c467e5c47a9dc04d0cbe93afcf300))
* docker build  paths & naming ([3c77ca4](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/3c77ca4097bff211968213c115b7ed8b3d9d3657))
* docker build  paths & naming ([7924a2e](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/7924a2e01b97f8c7a5a3795298a05428cdf2f9ca))
* docker file permissions & preservation ([951f030](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/951f0304cff2b6ab5bf435554fa47fc8efb04a55))
* don't preserve owner for data import ([bad0205](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/bad0205cdc40c40d8c3d73813cf39ea895ac4400))
* double / for openapi endpoint ([444ed0c](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/444ed0c8069d3729d893e247b335c7ea25fbfe97))
* exclude charts dir (templating/install) ([38b3198](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/38b319833c3039ab9b9f5cd1f128f83cd27b60a7))
* frontend relative build context ([9bcdc9d](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/9bcdc9de54ac7eb03b682ae1fff4c3f14c1ccfbf))
* frontend relative build context ([7ef043d](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/7ef043d8f95092f6ad317df463932372f5defcad))
* improve error handling & output for keycloak conn ([3136404](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/3136404a2a8c0e39ea14e91189e44fdd4995c242))
* move 2fa admin checker to correct section ([1e83923](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/1e839239fe68d19aadc1831c5b8acd541d3c3ca1))
* move helm chart to subdir & delete extra ci ([89fe9ce](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/89fe9ce0166314ff6cbc15c680f05cc78701ff42))
* move helm chart to subdir & delete extra ci ([939e2f8](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/939e2f8aec247ed9a47ee6484d81aaa696360729))
* openapi Readme content & helper container ([adff9d9](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/adff9d968686e027b71d0998dccc0de37e373a01))
* remove dark theme support and simplify color scheme ([457a203](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/457a2035622bdef2b5300cce9b7a4c4beb705d7f))
* remove dark theme support and simplify color scheme ([02ff039](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/02ff0396b5c4bc6b9edd6b526d7792a9f431b805))
* remove errors ([3d339fc](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/3d339fc3896881d993e374745df1a1ae509cd06d))
* remove obsolete Dockerfile ([7e1d6ff](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/7e1d6ff911e6ad4ccaa9814acb7b3f1dac3b8eee))
* remove obsolete port redirect ([8e5fb0d](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/8e5fb0d03a23122dc3a08fa61d3c6da546e87547))
* rename .env example ([efefdc6](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/efefdc6474d2ca1c365158b781d70ab814852caa))
* rename .env example ([bc5960c](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/bc5960ca472fe2823195fbba259247b9df3d55e7))
* repository rename ([f8fe377](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/f8fe377f177b8f9931e0e26018e2f4d7f08c5865))
* repository rename ([57754b7](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/57754b7cb809eb3048200301d21c2183c2313018))
* seperate own workdir for non-root kubernetes ([6128203](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/612820312fbfce7c6066672d26a346151b1f73a1))
* set subpath for frontend app ([9c99ba7](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/9c99ba7f9537ce321bb6ddb68a7848a112c12f19))
* speed up docker (re-)build ([329d5c3](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/329d5c3180b65c34ec607a4f36a6767f52dada72))
* ts check ([3ebcd39](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/3ebcd39ecafe39e7359174f1038ada571285bf71))
* ts check ([99d6067](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/99d606760c38778d08d9e20126daebd5b7763a35))
* typo (missing s) ([f54dcd7](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/f54dcd70fbf6e3ab4a91c25c3f0069cd138ad399))
* typo in admin groups var ([177bdfb](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/177bdfb3411558f0da67aeacabffa8a8bfc4f6d9))
* ucs dockerfile with fastapi ([f8a92d4](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/f8a92d4f06b587399a1152c946f48c38b3a50d50))
* update dependencies ([cef0578](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/cef05784b4b1ff858b3ebf45af3566c2c8fb5f2f))
* update dockerfile base image ([31d2ca3](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/31d2ca3d24ab6e08384143928900f76fbc3d14b6))
* update dockerfile base image ([0159cd7](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/0159cd71235402022a5d743140ae77d28a3e7a1f))
* update translation function usage and correct success message ([347e3ed](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/347e3ed528d73c1f8484fc030a793e56568eb5c0))
* use correct (new) udm python-lib ([5193b66](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/5193b66c015b45d03b08be2e5ca449fdc0b1b247))
* use correct keycloak secret ([16f075d](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/16f075d38c25f324546f9424b6713d34321ff8e4))
* use tag with build stale identifier ([4c82796](https://git.knut.univention.de/univention/dev/projects/2fa-helpdesk/commit/4c82796e60c0faab53147db50a8a77a7f37d2b80))

# 1.0.0 (2025-02-24)


### Features

* initial project skeleton WP 237 ([5995a5c](https://gitlab.opencode.de/bmi/opendesk/components/platform-development/images/opendesk-2fa-admin-backend/commit/5995a5cf40501b40be7818fdd24b62fdd0680f84))
