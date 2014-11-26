SOF15
=====

Driftmiljön
-----------
*Obs! Detta stämmer inte riktigt längre, men får stå kvar ett tag till då Vagrant-miljön ser ut ungefär så här.*

Systemet kommer snurra i en gammal beräkningsserver från NSC som lånas ut av LiTHe Blås. Det finns gott om kraft och 
minne så därför passar vi på att gödsla med dedicerade virtuella servrar enligt följande struktur:

* Chip
    * Django-applikationer
    * gunicorn
    * supervisor
    * Celery (vid behov)
    * memcached
* Dale
    * Sentry
    * gunicorn
    * supervisor
    * Celery
    * memcached
* Gadget
    * PostgreSQL
    * RabbitMQ
    * redis
* Zipper
    * nginx
        * Agerar reverse proxy till tjänsterna, inkl. Sentry
        * Servar statiska filer till tjänsterna och eventuella tunga filer som annars skulle läggas på hemsidan

Utvecklingsmiljön och Vagrant
-----------------------------
Vagrant är ett trevligt verktyg som gör det enkelt(!) att distribuera kompletta utvecklingsmiljöer. I det här fallet 
används det också för att på ett jätteautomatiserat sätt replikera driftmiljön med flera virtuella servrar på en simpel 
utvecklingsburk.

Du kommer igång genom att ladda ned och installera [Vagrant](https://www.vagrantup.com/downloads.html) respektive 
[VirtualBox](https://www.virtualbox.org/wiki/Downloads) för din plattform. När det är gjort ställer du dig i roten för 
detta projekt (dvs. katalogen som heter SOF15) och kör i ett skal `vagrant up`. Det kommer nu hämtas en Ubuntu-image och
skapas fyra stycken virtuella burkar som kör ett gäng olika konfigurationsskript. Det tar sin goda stund så ta en kopp 
kaffe under tiden. Klart!

### Några användbara kommandon
* `vagrant up [chip|dale|gadget|zipper]` Startar alla eller en specifik maskin. Skapar och konfigurerar denna/dessa vid 
  behov.
* `vagrant ssh chip|dale|gadget|zipper` Ger dig en SSH-session till respektive burk.
* `vagrant halt [chip|dale|gadget|zippr]` Stoppar alla eller en specifik maskin.
* `vagrant destroy [chip|dale|gadget|zipper]` Raderar alla eller en specifik maskin.

