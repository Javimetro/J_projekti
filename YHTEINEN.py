import mysql.connector
from geopy.distance import geodesic
from geopy import distance
import random

yhteys = mysql.connector.connect(
         host='127.0.0.1',
         port=3306,
         database='flight_game',
         user='root',
         password='123',
         autocommit=True
         )


def updatelocation(icao):
    sql = '''UPDATE game SET location= %s WHERE screen_name = "Phileas Fogg"'''
    tuple = (icao,)
    kursori = yhteys.cursor()
    kursori.execute(sql,tuple)
    if kursori.rowcount == 1:
        print("LOCATION UPDATED")


def haelongitude():
    sql = '''select longitude_deg
    from airport, game
    where screen_name = "Phileas Fogg" and location = ident'''
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchone()
    return tulos


def haelatitude():
    sql = '''select latitude_deg
    from airport, game
    where screen_name = "Phileas Fogg" and location = ident'''
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchone()
    return tulos


def valikoima():
    northlimit = lat1[0] + kilometrit * 0.01
    southlimit = lat1[0] - kilometrit * 0.01
    westlimit = lon1[0]
    eastlimit = lon1[0] + kilometrit * 0.01
    if southlimit < 0:
        southlimit = 0
    if northlimit > 80:
        northlimit = 80
    if -180 < eastlimit < 180:
        sql = f'''SELECT ident, name, latitude_deg, longitude_deg
            FROM Airport WHERE latitude_deg BETWEEN {southlimit} AND {northlimit}
            AND longitude_deg BETWEEN {westlimit} AND {eastlimit}'''
    elif eastlimit > 180:
        eastlimit = eastlimit - 360

        sql = f'''SELECT ident, name, latitude_deg, longitude_deg
            FROM Airport WHERE latitude_deg BETWEEN {southlimit} AND {northlimit}
            AND longitude_deg BETWEEN {-180} AND {eastlimit} AND {westlimit} AND {180}'''

    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchall()
    return tulos


def vaihtoehdot():
    vaihtoehdot1 = []
    tulos = valikoima()
    for i in range(4):
        vaihtoehdot1.append(random.choice(tulos))
    return vaihtoehdot1


def etaisyysicaolla(icao):
    tuple = (icao,)
    sql = '''SELECT latitude_deg, longitude_deg 
    FROM airport 
    WHERE ident = %s'''
    kursori = yhteys.cursor()
    kursori.execute(sql, tuple)
    tulos = kursori.fetchone()
    return tulos


def phileaslocation():
    sql = '''select latitude_deg, longitude_deg
    from airport, game
    where screen_name = "Phileas Fogg" and location = ident'''
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchone()
    return tulos


def londoncityairport():
    sql = '''select ident, name, latitude_deg, longitude_deg
        from airport
        where ident = "EGLC"'''
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchone()
    return tulos


def city_country():
    sql = '''select airport.municipality, country.name from airport, country, game 
    where screen_name='Phileas Fogg' and  game.location=airport.ident and airport.iso_country=country.iso_country;'''
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchall()
    for i in tulos:
        print(f'{i[0]} ,{i[1]}')


def onkoAlennusAlue(icao):
    tuple = (icao,)
    sql = '''SELECT latitude_deg FROM airport 
    WHERE ident = %s'''
    kursori = yhteys.cursor()
    kursori.execute(sql, tuple)
    tulos = kursori.fetchone()
    if 20 < tulos[0] < 40:
        print('Olet alennusalueella. Saat 50% alennusta.')
        return 0.5
    elif 40 <= tulos[0] <= 60:
        print('Matkasi hinta on suoraan verrannollinen kuljettuun matkaan.')
        return 1
    elif 0 < tulos[0] < 20:
        print('Olet alennusalueella. Saat 70% alennusta.')
        return 0.3
    elif 60 < tulos[0] < 80:
        print('Olet korkeammalla alueella. Joudut maksamaan 30% enemm??n.')
        return 1.3


def hintakaava(km):
    hinta = km/10 * onkoAlennusAlue(icao2)
    return hinta


def lisaraha(hinta):
    raha = hinta * 0.5
    return raha


def aloitusbudjetti():
    sql = f'''UPDATE game SET co2_budget=1000 WHERE id=1'''
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchone()
    return tulos


def hae_budjetti():
    sql = f'''SELECT co2_budget FROM game WHERE id=1'''
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchone()
    return tulos[0]


def paivita_budjetti(hinta,raha):
    sql = f'''UPDATE game SET co2_budget=co2_budget-{hinta}+{raha} WHERE id=1'''
    kursori=yhteys.cursor()
    kursori.execute(sql)
    tulos=kursori.fetchone()
    return tulos


def tarkista_budjetti():
    sql = f'''SELECT co2_budget FROM game WHERE id=1'''
    kursori=yhteys.cursor()
    kursori.execute(sql)
    tulos=kursori.fetchone()
    return tulos[0]


vuorot = 0
lopullinenbudjetti = 0
updatelocation('EGLC')
aloitusbudjetti()
lat1 = haelatitude()
lon1 = haelongitude()
print("Olet maailmankuulu maailmanmatkaaja Phileas Fogg ja sinut on haastettu matkustamaan maailman ymp??ri niin nopeasti kuin pysyt."
      "\nLenn??t maailman ymp??ri valitsemalla haluamasi matkan pituuden, mutta muista ett?? pide??mm??t matkat ovat kalliimpia!"
      "\nAloitat kotoasi Lontoosta ja sinne haluat my??s palata voittaaksesi."
      "\nOnnea matkaan, toivottavasti reisussa kest???? t??ll?? kertaa v??hemm??n kuin 80 p??iv????!\n")
input('-Paina n??pp??int?? ja aloitetaan matka-')
print(f'Olet nyt London City Airportilla ja koordinaattisi ovat: {lat1[0],lon1[0]}')
budjetti = hae_budjetti()
aloitusbudjetti = hae_budjetti()
print(f"Budjettisi on alussa {budjetti}???. T??m??n lis??ksi saat joka matkan j??lkeen hieman lis??rahaa.")
input('')
print('Ennen kuin aloitat matkasi, on t??rke????, ett?? sinulla on tietoa lippujen hinnoista ja niiden suhteesta et??isyyksiin.'
      "\nMatkasi hinta riippuu leveysasteista, joiden v??lill?? lenn??t.")
input('')
print('*Leveysasteet 40-60: Matkakustannukset ovat suoraan verrannollisia matkan pituuteen, koska l??ht??- ja tulopaikka sijaitsevat t??ll?? alueella.')
input('')
print('*Leveysasteet 20-40: N??ill?? alueilla matkasi hinta on 30 prosenttia halvempi, mutta matka voi kest???? hieman kauemmin.'
      '\nMaapallon ymp??rill?? oleva matka alkaa pidenty?? koska meridiaanien v??linen et??isyys on suurempi kuin Lontoossa.')
input('')
print('*Leveysasteet 0-20: T????ll?? liput ovat todella halpoja (70 % alennus!), mutta matka maapallon ymp??ri on kaikista pisin. Lenn??t l??hell?? p??iv??ntasaajaa.')
input('')
print('*Leveysasteet 60-80: T??m?? alue on l??hell?? pohjoisnapaa, ja t????ll?? ei kest?? kauan lent???? maailman ymp??ri (meridiaanien v??linen et??isyys on hyvin pieni). '
      '\nT??st?? syyst?? liput ovat 30 prosenttia kalliimpia.')
input('')

yht_etaisyys = 0
while budjetti > 0:
    kilometrit = int(input(f'Kuinka monta kilometri?? haluaisit lent????? '))

    print(f'Sill?? et??isyydell?? voit matkustaa seuraaville lentokentille:\n')
    tulos = vaihtoehdot()

    if yht_etaisyys > 5000:
        lontoo = londoncityairport()
        etaisyysLCA = distance.distance(phileaslocation(), lontoo[2:])
        print(f'et??isyys Lontoosta: {etaisyysLCA}\n')
        if -50 < lon1[0] < 5 and kilometrit >= etaisyysLCA:
            tulos.append(lontoo)

    i = 1
    for n in tulos:
        print(f'{i}: {n}')
        i = i + 1

    mihin = input(f'\n Valitse niist?? yksi ja matkustetaan sille lentokent??lle. Kirjoita numero:  ')

    phileaslocation()
    icao2 = tulos[int(mihin) - 1][0]

    km = round(geodesic(phileaslocation(), etaisyysicaolla(icao2)).km, 3)
    print(f' Et??isyys lentokenttien v??lill?? on: {km} Km.')

    hinta = hintakaava(km)
    print(f'Valitulle lentoasemalle l??htev??n lennon hinta on {hinta:.2f} ???')
    print(f'Valitusta lennosta saamasi lis??raha on {lisaraha(hinta):.2f} ???')


    varmistus = input(f'Oletko varma, ett?? haluat matkustaa {icao2} lentokent??lle (K/E)?: ')
    if varmistus == 'K':

        print('')
        paivita_budjetti(hinta, lisaraha(hinta))
        budjetti = tarkista_budjetti()
        if budjetti < 0:
            print('Upsis! Sinulla ei ole rahaa en????. Peli ohi :(')
            break
        updatelocation(icao2)
        city_country()
        lat1 = haelatitude()
        lon1 = haelongitude()
        print('')

        lopullinenbudjetti = lopullinenbudjetti + hinta
        yht_etaisyys = yht_etaisyys + km
        vuorot += 1

        if phileaslocation() == (51.505299, 0.055278):
            print(f'Onneksi olkoon! Olet p????ssyt takaisin Lontooseen! \nLensit yhteens?? {vuorot} kertaa, kilometrej?? kertyi yhteens?? {yht_etaisyys} ja k??ytit {lopullinenbudjetti:.2f}??? verran rahaa')
            break
        else:
            print(f'No niin, nyt sinun koordinaattisi ovat {lat1[0], lon1[0]}, budjettisi on {budjetti:.2f} ???')
    else:
        print("Oho! Ehk?? budjettisi ei riit??... Ei haittaa! Yritet????n uudestaan. Valitse uusi vaihtoehto, joka sopii paremmin.")
