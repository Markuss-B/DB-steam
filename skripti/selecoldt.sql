select * from Spēle where Versija like '0.%'
select top(50) * from SpēleŽanrs
select * from Lietotājs order by Izveidots asc

select * from Draudzējas
join Lietotājs on Lietotājs1 = Lietotājs.ID or Lietotājs2 = Lietotājs.ID
where Lietotājs.Izveidots > Datums

select * from LietotājaKategorija order by LietotājsID, Nosaukums
select * from LietotājaKategorija

select count(*) from LietotājsSpēle where LietotājsSpēle.SpēleID = 12

select * from LietotājsSasniegums

--
select count(*) from Spēle
select count(*) from Lietotājs

select ID, IzdošanasDatums from spēle order by Spēle.IzdošanasDatums

select * from LietotājsSpēle
join Spēle on LietotājsSpēle.SpēleID = Spēle.ID
where LietotājsSpēle.InstalētāVersija = Spēle.Versija

select * from VēlmjuSaraksts order by LietotājsID, Secība

select Nosaukums from Izstrādātājs
select Nosaukums from Izplatītājs
select Nosaukums from Žanrs

select LietotājsID, SpēleID from LietotājsSpēle

select ID,SpēleID from Sasniegums


select LietotājsID, IegūšanasDatums, count(*) from LietotājsSpēle
group by LietotājsID, IegūšanasDatums

select LietotājsID, SpēleID, IegūšanasDatums from LietotājsSpēle

select * from LietotājsSpēle where InstalētāVersija > '2.0.0'
select * from Spēle where Cena > 80

-- pirkums ar pirkumaspele
select * from Pirkums
join PirkumaSpēle on PirkumaSpēle.PirkumsID = Pirkums.ID

-- pirkums ar speli no lietotajsspele
select * from Pirkums
join LietotājsSpēle on LietotājsSpēle.IegūšanasDatums = Pirkums.Datums

-- kam nav atsauksmes
select LietotājsID, Lietotājs.ID from Recenzija
right join Lietotājs on Lietotājs.ID = Recenzija.LietotājsID
group by LietotājsID, Lietotājs.ID

select * from Žanrs where Nosaukums like 'Multiplayer'

-- Multiplayer spēles
select * from SpēleŽanrs
join Spēle on Spēle.ID = SpēleŽanrs.SpēleID
where ŽanrsNosaukums like 'Multiplayer'

select SpēleID from SpēleŽanrs
where ŽanrsNosaukums like 'Multiplayer'

select * from SpēleŽanrs

-- serveris un speles nosaukums
select Serveris.*, Spēle.Nosaukums from Serveris
join Spēle on Spēle.ID = SpēleID

select ID, SpēleID from Serveris

select Lietotājs1, Lietotājs2, LietotājsSpēle.SpēleID, s.SpēleID from Draudzējas
join LietotājsSpēle on Lietotājs1 = LietotājsSpēle.LietotājsID
join LietotājsSpēle s on Lietotājs2 = s.LietotājsID
where LietotājsSpēle.SpēleID = s.SpēleID

select * from LietotājsSpēlē

select id, spēleid from MantasKlase

select * from MantasKlase
select * from Manta
select * from MantasĪpašniekuVēsture

-- iegūsts iepriekšējos īpašniekus
select * from Manta
left join MantasĪpašniekuVēsture on MantasĪpašniekuVēsture.MantaID = Manta.ID

-- atlasa lietotāju spēles
select * from LietotājsSpēle

-- atlasa lietotāja bibliotēkas informāciju
-- spēļu skaits
select Lietotājs.ID, Niks, count(*) as SpēļuSkaits from LietotājsSpēle
join Lietotājs on LietotājsSpēle.LietotājsID = Lietotājs.ID
group by Lietotājs.ID, Niks

-- iecienītas spēles
select Lietotājs.ID, Niks, Spēle.ID, Spēle.Nosaukums from LietotājsSpēle
join Lietotājs on LietotājsSpēle.LietotājsID = Lietotājs.ID
join Spēle on LietotājsSpēle.SpēleID = Spēle.ID
where irIecienīta = 1

-- Visvairāk spēlētās spēles stundas
SELECT
	LietotājsID,
	Niks, 
	max(SpēlētāsStundas) as Stundas 
FROM LietotājsSpēle
JOIN Lietotājs on LietotājsSpēle.LietotājsID = Lietotājs.ID
GROUP BY LietotājsID, Niks
-- Lietotāja visvairāk spēlētā spēle ar spēles stundām. Var būt vairākas spēles ar lielāko stundu skaitu, bet datos tādi lietotāji neparādās
SELECT 
	Lietotājs.ID, 
	Lietotājs.Niks, 
	Spēle.Nosaukums, 
	MaxStundas.Stundas 
FROM
	(
	SELECT
		LietotājsID,
		Niks, 
		max(SpēlētāsStundas) as Stundas 
	FROM LietotājsSpēle
	JOIN Lietotājs on LietotājsSpēle.LietotājsID = Lietotājs.ID
	GROUP BY LietotājsID, Niks
	) as MaxStundas
JOIN LietotājsSpēle on MaxStundas.LietotājsID = LietotājsSpēle.LietotājsID and MaxStundas.Stundas = LietotājsSpēle.SpēlētāsStundas
JOIN Lietotājs on LietotājsSpēle.LietotājsID = Lietotājs.ID
JOIN Spēle on LietotājsSpēle.SpēleID = Spēle.ID
ORDER BY Lietotājs.ID

-- Draugu kopīgās spēles
SELECT Lietotājs1, Lietotājs2, ls1.SpēleID, ls2.SpēleID from Draudzējas
JOIN LietotājsSpēle as ls1 on ls1.LietotājsID = Lietotājs1
JOIN LietotājsSpēle as ls2 on ls2.LietotājsID = Lietotājs2
WHERE ls1.SpēleID = ls2.SpēleID
-- ar vārdiem un nosaukumiem
SELECT 
	Lietotājs1, 
	l1.Niks, 
	Lietotājs2, 
	l2.Niks, 
	Spēle.Nosaukums 
FROM Draudzējas
JOIN LietotājsSpēle as ls1 on ls1.LietotājsID = Lietotājs1
JOIN LietotājsSpēle as ls2 on ls2.LietotājsID = Lietotājs2
JOIN Lietotājs as l1 on l1.ID = Lietotājs1
JOIN Lietotājs as l2 on l2.ID = Lietotājs2
JOIN Spēle on Spēle.ID = ls1.SpēleID
WHERE ls1.SpēleID = ls2.SpēleID

-- varbūt draudzības vajag taisīt tā ka draudzībai tiek veltītas 2 rindiņas
-- konkrēta lietotājo draugi
select * from Draudzējas
where Lietotājs1 = 1007 or Lietotājs2 = 1007
-- konkrēta lietotāja draugu draugi
select * from Draudzējas as d
join Draudzējas as dd on dd.Lietotājs1 != 1007 and dd.Lietotājs2 != 1007
where d.Lietotājs1 = 1007 or d.Lietotājs2 = 1007
		and (dd.Lietotājs1 = d.Lietotājs1 or dd.Lietotājs1 = d.Lietotājs2 or dd.Lietotājs1 = d.Lietotājs2 or dd.Lietotājs1 = d.Lietotājs2)


SELECT 
    CASE 
        WHEN Lietotājs1 = 1007 THEN Lietotājs1 
        ELSE Lietotājs2 
    END AS Lietotājs,
    CASE 
        WHEN Lietotājs1 = 1007 THEN Lietotājs2 
        ELSE Lietotājs1 
    END AS Draugs,
    Datums 
FROM Draudzējas
WHERE Lietotājs1 = 1007 OR Lietotājs2 = 1007;


-- drauga kopīgie draugi
select * from Draudzējas
select Draudzējas.Lietotājs1, Draudzējas.Lietotājs2, dd.Lietotājs1, dd.Lietotājs2 from Draudzējas
left join Draudzējas as dd on dd.Lietotājs1 = Draudzējas.Lietotājs2 or dd.Lietotājs2 = Draudzējas.Lietotājs2
where dd.Lietotājs2 in (select Lietotājs2 from Draudzējas as d1 where d1.Lietotājs1 = Draudzējas.Lietotājs1)
	

select Draudzējas.Lietotājs1 as Lietotājs, Draudzējas.Lietotājs2 as Draugs, dd.Lietotājs2 as KopīgsDraugs from Draudzējas
join (select Lietotājs1 ,Lietotājs2 from Draudzējas) as dd on dd.Lietotājs1 = Draudzējas.Lietotājs1
-- drauga draugi
select * from Draudzējas
select Draudzējas.Lietotājs1, Draudzējas.Lietotājs2, dd.Lietotājs1, dd.Lietotājs2 from Draudzējas
join Draudzējas as dd on dd.Lietotājs1 = Draudzējas.Lietotājs2