# A crime has taken place and the detective needs your help. 
# The detective gave you the crime scene report, but you somehow lost it. 
# You vaguely remember that the crime was a ​murder​ that occurred sometime on ​Jan.15, 2018​ and that it took place in ​SQL City​. 
#  Start by retrieving the corresponding crime scene report from the police department’s database.

# query para obtener todas las tablas
'''
SELECT name 
  FROM sqlite_master
 where type = 'table'''

# ataco a la tabla de 'crime_scene_report' filtrando por:
# ​murder​ on ​Jan.15, 2018​ in ​SQL City 
'''
SELECT *
FROM crime_scene_report
WHERE date = ('20180115')
AND type = "murder"
AND city = "SQL City"
'''
# Security footage shows that there were 2 witnesses. 
# The first witness lives at the last house on "Northwestern Dr". 
# The second witness, named Annabel, lives somewhere on "Franklin Ave"


# llamada para obtener info del sospechoso 1 --> ataco a person filtrando por la calle y el último número:
# "lives at the last house on "Northwestern Dr"
'''
SELECT *
FROM person
WHERE address_street_name = 'Northwestern Dr'
ORDER BY address_number DESC
LIMIT 1;
'''
# 14887	Morty Schapiro	118009	4919	Northwestern Dr	111564949


# llamada para obtener la info del sospechoso2 --> ataco por la calle. intenté hacerlo por 'Annabel' per no me encuentra registros porque la columna name es nombre+apellido
'''
SELECT *
FROM person
WHERE address_street_name = ('Franklin Ave')
ORDER BY address_number DESC;
'''
# su info es: 16371	Annabel Miller	490173	103	Franklin Ave	318771143


# la estrategia es acceder a la tabla interview para ver sus declaraciones
# para ello, necesito el 'person_id', que es el mismo que el id en la tabla person'

# interview de Morty
'''
SELECT *
FROM interview
WHERE person_id = 16371
'''
# I heard a gunshot and then saw a man run out. He had a "Get Fit Now Gym" bag. 
# The membership number on the bag started with "48Z". 
# Only gold members have those bags. The man got into a car with a plate that included "H42W"


# interview de Annabel
'''
SELECT *
FROM interview
WHERE person_id = 16371
'''
#I saw the murder happen, and I recognized the killer from my gym when 
# I was working out last week on January the 9th


# a partir del relato de Morty:
# busco en la tabla de miembros del gym usuarios que su id empeice por "48Z"
'''
SELECT *
FROM get_fit_now_member
WHERE id LIKE '48Z%';
'''
# 48Z38	49550	Tomas Baisley	20170203	silver
# 48Z7A	28819	Joe Germuska	20160305	gold
# 48Z55	67318	Jeremy Bowers	20160101	gold


# a partir del relato de Morty y de los usuarios que su id empieza por '48z'
# ataco a drivers_license flitrando por plate number que contiene 'h42'
'''
SELECT *
FROM drivers_license
WHERE plate_number LIKE '%H42W%';

'''
# id	    age	height	  eye_color	      hair_color	gender	plate_number	car_make	   car_model
# 183779	21	65	       blue	          blonde	    female	H42W0X	       Toyota	      Prius
# 423327	30	70	       brown	        brown	        male	0H42W2	        Chevrolet	  Spark LS
# 664760	21	71	       black	        black	      male	4H42WR	          Nissan	    Altima


# ahora llamo a la tabla persons para saber el nombre de los sospechosos
# a partir de del license_ID:
'''
SELECT *
FROM person
WHERE license_Id IN (183779, 423327, 664760);
'''
# id	     name	                license_id	      address_number	     address_street_name	     ssn
# 51739	  Tushar Chandra	       664760	             312	                 Phi St	                 137882671
# 67318	  Jeremy Bowers	            423327	         530	                 Washington Pl, Apt 3A	  871539279
#78193	  Maxine Whitely	          183779	         110	                  Fisk Rd	                137882671


# el sospechoso principal es Jeremy Bowers:
# es hombre
# es miembro gold del gym
# su matrícula contiene los números 'h42'
# su id del gym empieza por '48z'


# hago una llamada para revisar su interview a través de su person_id
'''
SELECT *
FROM interview
WHERE person_id = 67318;
'''
# I was hired by a woman with a lot of money. 
# I don't know her name but I know she's around 5'5" (65") or 5'7" (67"). 
# She has red hair and she drives a Tesla Model S. 
# I know that she attended the SQL Symphony Concert 3 times in December 2017

# busco a la persona que describe en la tabla license_Id:
'''             
SELECT *
FROM drivers_license
WHERE hair_color = 'red'
  AND height BETWEEN 65 AND 67
  AND car_make = 'Tesla'
  AND gender = 'female';
'''
#   id	       age	          height	       eye_color	    hair_color	   gender	   plate_number	   car_make	     car_model
#  202298	     68	            66	           green	          red	         female	    500123	        Tesla	        Model S
#  291182	     65	            66	            blue	          red	          female	  08CM64	        Tesla	        Model S
#  918773	     48	            65	            black	          red	          female	   917UU3	        Tesla	        Model S



# vuelvo a llamar a tabla person para obtener los nombres de las tres sospechosas:
'''
SELECT *
FROM person
WHERE license_Id IN (202298, 291182,  918773);
'''
#   id	    name	        license_id	        address_number	    address_street_name	      ssn
#   78881	  Red Korb	     918773	            107	                 Camerata Dr	            961388910
#   90700	   Regina George	291182	          332	                  Maple Ave	              337169072
#   99716	  Miranda Priestly 202298	          1883	                Golden Ave	            987756388

# Jeremy Bowers también decía que la soscheposa tenía mucho dinero y que había ido tres veces a un concierto, 
# primero compruebo lo del dinero a través del ssn atacando a la tabla income:

'''
SELECT *
FROM income
WHERE ssn IN (961388910, 337169072,  987756388);
'''
#  ssn	         annual_income
# 961388910	     278000    ---> Red Korb
# 987756388	     310000    ---> Miranda Priestly
# no he obtenido datos de la tercera sospechosa Regina George.


# ahora voy a comprobar si algunas de esas personas fue 3 veces al concierto:
'''
SELECT *
FROM facebook_event_checkin
WHERE person_Id IN (78881, 90700,  99716);
'''
# person_id	    event_id	         event_name	          date
#99716	        1143	             SQL Symphony Concert	20171206
#99716	        1143	             SQL Symphony Concert	20171212
#99716	        1143	             SQL Symphony Concert	20171229

# la potencial asesisina es Miranda Priestly:
# acudió 3 veces al SQL Symphony Concert en diciembre del 2017
# tiene un anual income de 310000

# Compruebo si es la asesina:
'''
INSERT INTO solution VALUES (1, 'Miranda Priestly');
        
        SELECT value FROM solution;
'''

# Congrats, you found the brains behind the murder! 
# Everyone in SQL City hails you as the greatest SQL detective of all time. Time to break out the champagne!