--------------------------------
-- 1. Lietotāja spēles
--
SELECT Lietotājs.ID, Niks, SpēleID, Spēle.Nosaukums, irIecienīta, SpēlētāsStundas, IegūšanasDatums, IzdošanasDatums, InstalētāVersija, Versija, Izstrādātājs, Izplatītājs FROM Lietotājs
LEFT JOIN LietotājsSpēle on LietotājsSpēle.LietotājsID = Lietotājs.ID
LEFT JOIN Spēle on Spēle.ID = LietotājsSpēle.SpēleID
ORDER BY Lietotājs.ID, irIecienīta desc
-- Lietotāja spēles lietotājiem kam ir spēles
SELECT LietotājsID, Niks, SpēleID, Spēle.Nosaukums, irIecienīta, SpēlētāsStundas, IegūšanasDatums, IzdošanasDatums, InstalētāVersija, Versija, Izstrādātājs, Izplatītājs
FROM LietotājsSpēle
JOIN Lietotājs on Lietotājs.ID = LietotājsID
JOIN Spēle on Spēle.ID = SpēleID
ORDER BY LietotājsID, irIecienīta desc

-- iecienītas spēles
select Lietotājs.ID, Niks, Spēle.ID, Spēle.Nosaukums, LietotājsSpēle.SpēlētāsStundas from LietotājsSpēle
join Lietotājs on LietotājsSpēle.LietotājsID = Lietotājs.ID
join Spēle on LietotājsSpēle.SpēleID = Spēle.ID
where irIecienīta = 1

-- 1.2 Lietotāja definētās kategorijas ar spēlēm tajās
SELECT Lietotājs.ID, Niks, LietotājaKategorija.ID as KetegorijasID, LietotājaKategorija.Nosaukums as KategorijasNosaukums, SpēleID, Spēle.Nosaukums as SpēlesNosaukums
FROM LietotājaKategorija
left JOIN  LietotājaKategorijaSpēle on LietotājaKategorijaSpēle.LietotājsKategorijaID = LietotājaKategorija.ID
right JOIN Lietotājs on Lietotājs.ID = LietotājsID
left JOIN Spēle on Spēle.ID = SpēleID

-- Dokumentā 1.
-- Spēļu skaits lietotāja definētā kategorijā
SELECT LietotājsID, Niks, LietotājaKategorija.ID as KategorijasID, LietotājaKategorija.Nosaukums, COUNT(*) as SpēļuSkaits
FROM LietotājaKategorija
JOIN LietotājaKategorijaSpēle on LietotājaKategorijaSpēle.LietotājsKategorijaID = LietotājaKategorija.ID
JOIN Lietotājs on Lietotājs.ID = LietotājsID
GROUP BY LietotājsID, Niks, LietotājaKategorija.ID, Nosaukums

------------------------------------
-- 2. Lietotāja bibliotēkas apraksts
-- Visvairāk spēlētās spēles stundas, ja ir null tad nav spēles
drop view LietotājaMaxSpēlētāsStundas
CREATE VIEW LietotājaMaxSpēlētāsStundas as
SELECT
	Lietotājs.ID,
	Niks, 
	max(SpēlētāsStundas) as Stundas
FROM LietotājsSpēle
right JOIN Lietotājs on LietotājsSpēle.LietotājsID = Lietotājs.ID
GROUP BY Lietotājs.ID, Niks
-- 2.1 Lietotāja visvairāk spēlētā spēle ar spēles stundām. Un tās spēles visvairāk nospēlētās stundas. Tikai lietotāji ar spēlēm
SELECT 
	Lietotājs.ID, 
	Lietotājs.Niks, 
	Spēle.Nosaukums, 
	lmss.Stundas,
	(
	SELECT
		max(ls.SpēlētāsStundas)
	FROM LietotājsSpēle ls
	WHERE  ls.SpēleID = LietotājsSpēle.SpēleID
	) as LielākaisStunduSkaitsSpēlei
FROM
	LietotājaMaxSpēlētāsStundas lmss
JOIN LietotājsSpēle on lmss.ID = LietotājsSpēle.LietotājsID and lmss.Stundas = LietotājsSpēle.SpēlētāsStundas
JOIN Lietotājs on LietotājsSpēle.LietotājsID = Lietotājs.ID
JOIN Spēle on LietotājsSpēle.SpēleID = Spēle.ID
ORDER BY Lietotājs.ID
-- tas pats ar rank over
SELECT 
	LietotājsID,
	Niks, SpēleID, 
	Spēle.Nosaukums, 
	SpēlētāsStundas,
	(
	SELECT
		max(ls.SpēlētāsStundas)
	FROM LietotājsSpēle ls
	WHERE  ls.SpēleID = StunduVietas.SpēleID
	) as LielākaisStunduSkaitsSpēlei
FROM
	(
	SELECT *, DENSE_RANK() over (partition by LietotājsID order by SpēlētāsStundas desc) vieta 
	FROM LietotājsSpēle
	) as StunduVietas
JOIN Lietotājs on Lietotājs.ID = LietotājsID
JOIN Spēle on SpēleID = Spēle.ID
WHERE vieta = 1
ORDER BY LietotājsID

-- spēļu skaits
select Lietotājs.ID, Niks, count(SpēleID) as SpēļuSkaits from LietotājsSpēle
right join Lietotājs on LietotājsSpēle.LietotājsID = Lietotājs.ID
group by Lietotājs.ID, Niks
-- iecienītu spēļu skaits tiem kam ir spēles
select Lietotājs.ID, Niks, count(irIecienīta) IecienītuSpēļuSkaits from LietotājsSpēle
join Lietotājs on LietotājsSpēle.LietotājsID = Lietotājs.ID
join Spēle on LietotājsSpēle.SpēleID = Spēle.ID
where irIecienīta = 1
group by Lietotājs.ID, Niks


-- īss bibliotēkas apraksts
SELECT 
	Lietotājs.ID, 
	Lietotājs.Niks, 
	count(SpēleID) as SpēļuSkaits, 
	sum(cast(irIecienīta as int)) IecienītuSpēļuSkaits, 
	sum(SpēlētāsStundas) as KopāNospēlētāsStundas, 
	max(LietotājsSpēle.IegūšanasDatums) PēdējāIegūtāSpēle
FROM LietotājsSpēle
right JOIN Lietotājs on LietotājsSpēle.LietotājsID = Lietotājs.ID
GROUP BY Lietotājs.ID, Lietotājs.Niks

-- Lietotaja pēdējā iegūtā spēle
select LietotājsID, SpēleID, IegūšanasDatums from
(select *, ROW_NUMBER() over (partition by LietotājsID order by IegūšanasDatums desc) vieta from LietotājsSpēle) s
where vieta = 1

-- Dokumentā 2.
-- 2.2 Plašāks bibliotēkas apraksts.
-- Lietotājs, spēļu skaits, mīļāko spēļu skaits, vispār kopējās stundas pa visām spēlēm, spēle ar lielāko stundu skaitu, pēdējā iegūtā spēle, lietotāja populārakais žanrs un cik spēles ar to žanru
SELECT top(10)
	main.*,
	stund.SpēlētāsStundas LielākaisStunduSkaitsSpēlei,
	stund.Nosaukums VisspēlētākāSpēle,
	sub.IegūšanasDatums PēdējāSpēleIegūta,
	sub.SpēleID PēdējāsIegūtasSpēlesID,
	sub.Nosaukums PēdējāsIegūtasSpēlesNosaukums,
	žanrs.ŽanrsNosaukums PopulārākaisŽanrs,
	žanrs.SpēlesArŽanru SpēlesŽanrā,
	izstr.Izstrādātājs PopulārākaisIzstrādātājs,
	izstr.SpēļuSkaits SpēļuSkaitsNoIzstrādātāja
FROM
	(SELECT -- Spēļu skaits, iecienītu spēļu skaits un kopā nospēlētās stundas
		Lietotājs.ID, 
		Lietotājs.Niks, 
		count(SpēleID) as SpēļuSkaits, 
		sum(cast(irIecienīta as int)) IecienītuSpēļuSkaits, 
		sum(SpēlētāsStundas) as KopāNospēlētāsStundas
	FROM LietotājsSpēle
	RIGHT JOIN Lietotājs on LietotājsSpēle.LietotājsID = Lietotājs.ID
	GROUP BY Lietotājs.ID, Lietotājs.Niks) main
LEFT JOIN 
	(SELECT -- Lietotaja pēdējā iegūtā spēle
		LietotājsID, 
		SpēleID,
		Nosaukums,
		IegūšanasDatums 
	FROM
		( -- Saranko lietotāja spēles pēc iegādes datuma
		SELECT *, ROW_NUMBER() over (partition by LietotājsID order by IegūšanasDatums desc) vieta
		FROM LietotājsSpēle) s
	JOIN Spēle on Spēle.ID = SpēleID
	WHERE vieta = 1) sub on sub.LietotājsID = main.ID
LEFT JOIN
	(SELECT * -- Atlasa lietotāja populārāko žanru un piederošo spēļu skaitu ar to žanru
	FROM
		(SELECT -- saranko lietotāja žanrus pēc piederošo spēļu skaita
			LietotājsID, 
			ŽanrsNosaukums,
			count(*) SpēlesArŽanru,
			row_number() over (partition by LietotājsID order by count(*) desc) VietaPēcSpēļuSkaita
		FROM LietotājsSpēle
		JOIN Spēle on Spēle.ID = LietotājsSpēle.SpēleID
		JOIN SpēleŽanrs on SpēleŽanrs.SpēleID = LietotājsSpēle.SpēleID
		GROUP BY LietotājsID,ŽanrsNosaukums) žr
	WHERE žr.VietaPēcSpēļuSkaita = 1) žanrs on žanrs.LietotājsID = main.ID
LEFT JOIN
	(SELECT -- Atlasa lietotājā spēlētāko spēli un spēles nospēlēto stundu skaitu
		LietotājsID,
		SpēleID, 
		Spēle.Nosaukums, 
		SpēlētāsStundas
	FROM
		( -- Saranko lietotāja spēles pēc nospēlēto stundu skaita
		SELECT *, row_number() over (partition by LietotājsID order by SpēlētāsStundas desc) vieta 
		FROM LietotājsSpēle
		) as StunduVietas
	JOIN Lietotājs on Lietotājs.ID = LietotājsID
	JOIN Spēle on SpēleID = Spēle.ID
	WHERE vieta = 1) stund on stund.LietotājsID = main.ID
LEFT JOIN
	(SELECT * -- Atlasa lietotāja populārāko izstrādātāju pēc piederošo spēļu skaita
	FROM
		( -- Saranko lietotāja izstrādātājus pēc piederošo spēļu skaita
		SELECT LietotājsID, Izstrādātājs, count(*) SpēļuSkaits, DENSE_RANK() over (partition by LietotājsID order by count(*) desc) vieta
		FROM LietotājsSpēle
		JOIN Spēle on Spēle.ID = LietotājsSpēle.SpēleID
		GROUP BY LietotājsID, Izstrādātājs) apakšpieprasījums
	WHERE apakšpieprasījums.vieta = 1) izstr on izstr.LietotājsID = main.ID

-- 2.3 Bibliotēkas spēles sadalītas pēc žanriem
-- Kādi žanri pieejami lietotāja bibliotēkā un cik spēles ar attiecīgo žanru
SELECT 
	LietotājsID, 
	ŽanrsNosaukums,
	count(Spēle.ID) SpēlesArŽanru,
	dense_rank() over (partition by LietotājsID order by count(Spēle.ID) desc) VietaPēcSpēļuSkaita
FROM LietotājsSpēle
JOIN Spēle on Spēle.ID = LietotājsSpēle.SpēleID
JOIN SpēleŽanrs on SpēleŽanrs.SpēleID = LietotājsSpēle.SpēleID
GROUP BY LietotājsID,ŽanrsNosaukums
ORDER BY LietotājsID,ŽanrsNosaukums

-- Lietotāja populārākais žanrs
SELECT *
FROM
	(SELECT 
		Lietotājs.ID, 
		ŽanrsNosaukums,
		count(Spēle.ID) SpēlesArŽanru,
		dense_rank() over (partition by Lietotājs.ID order by count(*) desc) VietaPēcSpēļuSkaita
	FROM LietotājsSpēle
	JOIN Lietotājs on Lietotājs.ID = LietotājsID
	JOIN Spēle on Spēle.ID = LietotājsSpēle.SpēleID
	JOIN SpēleŽanrs on SpēleŽanrs.SpēleID = LietotājsSpēle.SpēleID
	GROUP BY Lietotājs.ID,ŽanrsNosaukums) žr
WHERE žr.VietaPēcSpēļuSkaita = 1

-- 2.4 Lietotāja spēļu izstrādātāji
-- izstrādātāji
SELECT LietotājsID, Izstrādātājs
FROM LietotājsSpēle
JOIN Spēle on Spēle.ID = LietotājsSpēle.SpēleID
GROUP BY LietotājsID, Izstrādātājs
-- Lietotāja populārākais izstrādātājs
SELECT * 
FROM
	(SELECT LietotājsID, Izstrādātājs, count(*) SpēļuSkaits, DENSE_RANK() over (partition by LietotājsID order by count(*) desc) vieta
	FROM LietotājsSpēle
	JOIN Spēle on Spēle.ID = LietotājsSpēle.SpēleID
	GROUP BY LietotājsID, Izstrādātājs) apakšpieprasījums
WHERE apakšpieprasījums.vieta = 1


------------------------------------------
-- 3. Draugi
-- Lietotāja draugi un draudzības datums
SELECT 
	l.id as ID, 
	l.Niks as Lietotājs, 
	d.id as DraugsID, 
	d.Niks as Draugs,
	dr1.Datums DraugiKopš
FROM Draudzējas dr1
right join Lietotājs l on l.ID = dr1.Lietotājs1
left join Lietotājs d on d.ID = dr1.Lietotājs2

-- Lietotāja draugu skaits un ilgākā draudzība
SELECT
	Lietotājs.ID,
	count(Lietotājs2) DrauguSkaits,
	min(Datums) IlgākāDraudzība
FROM Draudzējas
right join Lietotājs on Lietotājs.ID = Lietotājs1
GROUP BY Lietotājs.ID

-- 3.1 Lietotāja draugu draugi
SELECT 
	l.ID as ID, 
	l.Niks as Lietotājs, 
	d.ID as DraugsID, 
	d.Niks as Draugs,
	dd.ID as DraugaDraugsID, 
	dd.Niks as DraugaDraugs 
FROM Draudzējas dr1
right join Lietotājs l on l.ID = dr1.Lietotājs1
left join Lietotājs d on d.ID = dr1.Lietotājs2
left join Draudzējas dr2 on dr2.Lietotājs1 = dr1.Lietotājs2
left join Lietotājs dd on dd.ID = dr2.Lietotājs2
WHERE l.ID != dd.ID


-- 3.2 Lietotāja un drauga kopīgie draugi. Atlasa tikai ja ir kopīgie draugi
SELECT 
	l.ID as ID, 
	l.Niks as Lietotājs, 
	d.ID as DraugsID, 
	d.Niks as Draugs,
	dk.ID as DraugaDraugsID, 
	dk.Niks as DraugaDraugs 
FROM Draudzējas dr1
join Lietotājs l on l.ID = dr1.Lietotājs1
join Lietotājs d on d.ID = dr1.Lietotājs2
join Draudzējas dr2 on dr2.Lietotājs1 = dr1.Lietotājs2
join Draudzējas dr3 on dr3.Lietotājs1 = l.ID and dr3.Lietotājs2 = dr2.Lietotājs2
join Lietotājs dk on dk.ID = dr3.Lietotājs2
WHERE dk.ID != l.id
-- cits veids
SELECT 
	main.Lietotājs1 as ID, 
	l.Niks as Lietotājs, 
	main.Lietotājs2 as DraugsID, 
	d.Niks as Draugs, 
	sub.Lietotājs2 as KopīgaisDraugsID, 
	dd.Niks as KopīgaisDraugs 
FROM Draudzējas main
join Lietotājs l on l.ID = main.Lietotājs1
join Lietotājs d on d.ID = main.Lietotājs2
join Draudzējas sub on sub.Lietotājs1 = main.Lietotājs2 -- drauga draugi
join Lietotājs dd on dd.ID = sub.Lietotājs2
where sub.Lietotājs2 in (select ws.Lietotājs2 from Draudzējas ws where ws.Lietotājs1 = main.Lietotājs1) -- atlasa tikai ja ir kopīgs draugs 
	and main.Lietotājs1 != sub.Lietotājs2
order by main.Lietotājs1
-- ja nav kopīgo draugu parāda null, parāda arī tos kam nav draugu
SELECT 
    l.ID as ID, 
    l.Niks as Lietotājs, 
    d.ID as DraugsID, 
    d.Niks as Draugs,
    dd.ID as KopīgaisDraugsID, 
    dd.Niks as KopīgaisDraugs 
FROM Draudzējas dr1
RIGHT JOIN Lietotājs l on l.ID = dr1.Lietotājs1
LEFT JOIN Lietotājs d on d.ID = dr1.Lietotājs2
LEFT JOIN Draudzējas dr2 on dr2.Lietotājs1 = d.ID
LEFT JOIN Draudzējas dr3 on dr3.Lietotājs1 = l.ID and dr3.Lietotājs2 = dr2.Lietotājs2 -- common friends
LEFT JOIN Lietotājs dd on dd.ID = dr3.Lietotājs2
group by
	l.ID, 
    l.Niks, 
    d.ID, 
    d.Niks,
    dd.ID, 
    dd.Niks
ORDER BY l.ID, d.ID

-- Dokumentā 3.
-- Kopīgo draugu skaits, ja lietotājs un tā draugs neparādas tad tiem nav draugu
SELECT 
	dr1.Lietotājs1 as ID, 
	l.Niks as Lietotājs, 
	dr1.Lietotājs2 as DraugsID, 
	d.Niks as Draugs,
	count(*) KopīgoDrauguSkaits
FROM Draudzējas dr1
join Draudzējas dr2 on dr2.Lietotājs1 = dr1.Lietotājs2
join Lietotājs l on l.ID = dr1.Lietotājs1
join Lietotājs d on d.ID = dr1.Lietotājs2
join Lietotājs dd on dd.ID = dr2.Lietotājs2
where dr2.Lietotājs2 in (select ws.Lietotājs2 from Draudzējas ws where ws.Lietotājs1 = dr1.Lietotājs1) -- lai drauga draugs ir lietotāja draugu sarakstā
	and dr1.Lietotājs1 != dr2.Lietotājs2
group by 
	dr1.Lietotājs1,
	l.Niks,
	dr1.Lietotājs2,
	d.Niks
order by dr1.Lietotājs1

-- Dokumentā 4.
-- 3.3 Draugu kopīgās spēles
SELECT Lietotājs.ID,
	Lietotājs.Niks,
	Draugs.ID,
	Draugs.Niks,
	Spēle.ID,
	Spēle.Nosaukums
FROM Draudzējas
JOIN LietotājsSpēle as ls1 on ls1.LietotājsID = Lietotājs1
JOIN LietotājsSpēle as ls2 on ls2.LietotājsID = Lietotājs2
JOIN Lietotājs on Lietotājs.ID = Lietotājs1
JOIN Lietotājs Draugs on Draugs.ID = Lietotājs2
JOIN Spēle on Spēle.ID = ls1.SpēleID
WHERE ls1.SpēleID = ls2.SpēleID
ORDER BY Lietotājs.ID, Spēle.Nosaukums

---------------------------------
-- 4. Izstrādātāji
select * from Izstrādātājs
join Spēle on Spēle.Izstrādātājs = Izstrādātājs.Nosaukums

-- Izstrādātāju spēles
select Izstrādātājs.Nosaukums, Spēle.ID, Spēle.Nosaukums from Izstrādātājs
left join Spēle on Spēle.Izstrādātājs = Izstrādātājs.Nosaukums

-- Kāda žanra spēles izstrādātājs izstrādā un cik tāda žanra spēles izstrādā, bet parāda tikai ja spēļu skaits ir >2
select Izstrādātājs.Nosaukums, SpēleŽanrs.ŽanrsNosaukums, count(Spēle.ID) SpēlesArŽanru from Izstrādātājs
left join Spēle on Spēle.Izstrādātājs = Izstrādātājs.Nosaukums
left join SpēleŽanrs on SpēleŽanrs.SpēleID = Spēle.ID
group by Izstrādātājs.Nosaukums, ŽanrsNosaukums
having count(Spēle.ID) > 2
order by Izstrādātājs.Nosaukums, ŽanrsNosaukums

-- Dokumentā 5.
-- Izstrādātāja žanrs ar visvairāk spēlēm, parāda vairākus žanrus ja tādi ir vairāki
select *
from ( -- Saranko izstrādātāja žanrus pēc spēļu skaita -- labāk var redzēt pie izstrādātāja ar vairāk spēlēm (piemēram - valve)
select Izstrādātājs.Nosaukums, SpēleŽanrs.ŽanrsNosaukums, count(Spēle.ID) SpēlesArŽanru, dense_rank() over (partition by Izstrādātājs.Nosaukums order by count(Spēle.ID) desc) vieta from Izstrādātājs
left join Spēle on Spēle.Izstrādātājs = Izstrādātājs.Nosaukums
left join SpēleŽanrs on SpēleŽanrs.SpēleID = Spēle.ID
group by Izstrādātājs.Nosaukums, ŽanrsNosaukums) ss
where ss.vieta = 1

----------------------------
-- 5. Spēles
select * from Spēle
-- Cik lietotājiem pieder spēle un visu spēlētāju kopā nospēlētās spēles tajā spēlē
SELECT
	Spēle.ID,
	Spēle.Nosaukums,
	count(ls.LietotājsID) Lietotāji,
	sum(ls.SpēlētāsStundas) KopāNospēlētāsStundas
FROM Spēle
LEFT JOIN LietotājsSpēle ls on ls.SpēleID = Spēle.ID
GROUP BY Spēle.ID, Spēle.Nosaukums
ORDER BY Lietotāji desc, KopāNospēlētāsStundas desc

-- Cik pašreiz spēlē spēli
SELECT
	SpēleID,
	count(LietotājsID) Spēlē
FROM LietotājsSpēlē
GROUP BY SpēleID

-- abi kopā
-- Dokumentā 6.
-- 5.1 Spēles spēlētāju informācija t.i. cik lietotājiem spēle pieder, visu spēlētāju kopā nospēlētās stundas spēlē un cik šobrīd spēli spēlē
-- priekš view noņem order by
drop view SpēlesLietotājuInfo
CREATE VIEW SpēlesLietotājuInfo as
SELECT main.*, Spēlētāji.Spēlē FROM
	(
	SELECT -- Cik lietotājiem pieder spēle un kopā nospēlēto stundu skaits
		Spēle.ID,
		Spēle.Nosaukums,
		count(ls.LietotājsID) Lietotāji,
		sum(ls.SpēlētāsStundas) KopāNospēlētāsStundas
	FROM Spēle
	LEFT JOIN LietotājsSpēle ls on ls.SpēleID = Spēle.ID
	GROUP BY Spēle.ID, Spēle.Nosaukums) main
LEFT JOIN
	(SELECT -- Cik šobrīd spēlē spēli
		SpēleID,
		count(LietotājsID) Spēlē
	FROM LietotājsSpēlē
	GROUP BY SpēleID) Spēlētāji on Spēlētāji.SpēleID = main.ID
ORDER BY Lietotāji desc, KopāNospēlētāsStundas desc, Spēlē desc

-- Izstrādātāja populārākā spēle pēc īpašnieku skaita un kolonna ar īpašnieku skaitu nākamajai vispopulārākajai izstrādātāja spēlei pēc īpašnieku skaita
SELECT
	Izstrādātājs.Nosaukums,
	sli.*,
	lag(Lietotāji) over (partition by Izstrādātājs.Nosaukums order by Lietotāji) as 'Izstrādātāja otrās vispopulārākās spēles īpasnieku skaits'
FROM Izstrādātājs
LEFT JOIN Spēle on Spēle.Izstrādātājs = Izstrādātājs.Nosaukums
LEFT JOIN SpēlesLietotājuInfo sli on sli.ID = Spēle.ID
ORDER BY Lietotāji desc

-- Dokumentā 7.
-- 5.2 Žanra vispopulārākā spēle pēc lietotaju skaita
SELECT * FROM
	(
	SELECT -- saranka žanra spēles pēc īpašnieku skaita
		ŽanrsNosaukums,
		sli.*,
		DENSE_RANK() over (partition by ŽanrsNosaukums order by Lietotāji desc) vieta
	FROM SpēlesLietotājuInfo sli
	LEFT JOIN SpēleŽanrs sz on sz.SpēleID = sli.ID) ss
WHERE ss.vieta = 1
ORDER BY ŽanrsNosaukums

-----------------------------------------
-- 6. Mantas
select * from Manta

-- Dokumentā 8.
-- Lietotāja inventārs pēc spēlēm. Parāda mantas nosaukumu un doto vārdu un izveides datumu
SELECT
	Lietotājs.ID,
	Lietotājs.Niks,
	Spēle.ID SpēleID,
	Spēle.Nosaukums SpēleNosaukums,
	MantasKlase.ID MantasKlaseID,
	MantasKlase.Nosaukums MantasKlaseNosaukums,
	Manta.ID MantaID,
	Manta.DotaisVārds MantasĪpašniekaDotaisVārds,
	Manta.IzveidesDatums,
	MantasKlase.Apraksts
FROM Lietotājs
LEFT JOIN Manta on Manta.ĪpašnieksID = Lietotājs.ID
LEFT JOIN MantasKlase on MantasKlase.ID = Manta.MantasKlaseID
LEFT JOIN Spēle on Spēle.ID = MantasKlase.SpēleID
ORDER BY Lietotājs.ID, Spēle.ID

-- Inventāra informācija
-- Lietotāja kopējas mantu skaits
--SELECT
	Lietotājs.ID,
	Lietotājs.Niks,
	count(Manta.ID) over (partition by Lietotājs.ID) LietotājaKopējasMantuSkaits
FROM Lietotājs
LEFT JOIN Manta on Manta.ĪpašnieksID = Lietotājs.ID
-- Lietotāja mantu skaits spēlē
SELECT
	Lietotājs.ID,
	Lietotājs.Niks,
	Spēle.ID,
	Spēle.Nosaukums,
	count(Manta.ID) MantuSkaits
FROM Lietotājs
LEFT JOIN Manta on Manta.ĪpašnieksID = Lietotājs.ID
LEFT JOIN MantasKlase on MantasKlase.ID = Manta.MantasKlaseID
LEFT JOIN Spēle on Spēle.ID = MantasKlase.SpēleID
GROUP BY 
	Lietotājs.ID,
	Lietotājs.Niks,
	Spēle.ID,
	Spēle.Nosaukums
ORDER BY Lietotājs.ID, Spēle.ID

-- Mantas iepriekšējie īpašnieki
select * from MantasĪpašniekuVēsture
order by MantasĪpašniekuVēsture.MantaID

-- Dokumentā 9.
-- cik mantas klases instances eksistē
select MantasKlase.ID, MantasKlase.Nosaukums, count(Manta.ID) Instances from MantasKlase
left join Manta on Manta.MantasKlaseID = MantasKlase.ID
group by MantasKlase.ID, MantasKlase.Nosaukums
order by Instances desc

------------------------------------
-- 7. Serveri
-- Servera spēlētāji
SELECT
	Serveris.IPAddress,
	Serveris.Port,
	Serveris.Nosaukums,
	Lietotājs.ID,
	Lietotājs.Niks
FROM Serveris
LEFT JOIN LietotājsSpēlē on LietotājsSpēlē.ServerisID = Serveris.ID
LEFT JOIN Lietotājs on Lietotājs.ID = LietotājsSpēlē.LietotājsID
ORDER BY Serveris.IPAddress, Serveris.Port, Serveris.Nosaukums

-- Dokumentā 11.
-- Konkrēta servera spēlētāji
SELECT
	Lietotājs.ID,
	Lietotājs.Niks
FROM Serveris
LEFT JOIN LietotājsSpēlē on LietotājsSpēlē.ServerisID = Serveris.ID
LEFT JOIN Lietotājs on Lietotājs.ID = LietotājsSpēlē.LietotājsID
where IPAddress like '152.137.14.103' and port like '9638'

-- Dokumentā 10.
-- Servera informācija
-- Servera ip adrese, spēles nosaukums un spēlētāju skaits
-- sakārtots pēc spēlētāju skaita
SELECT
	Serveris.IPAddress,
	Serveris.Port,
	Serveris.Nosaukums,
	Spēle.ID,
	Spēle.Nosaukums,
	count(LietotājsID) Spēlētāji
FROM Serveris
LEFT JOIN Spēle on Spēle.ID = Serveris.SpēleID
LEFT JOIN LietotājsSpēlē on LietotājsSpēlē.SpēleID = Spēle.ID
GROUP BY
	Serveris.IPAddress,
	Serveris.Port,
	Serveris.Nosaukums,
	Spēle.ID,
	Spēle.Nosaukums
ORDER BY Spēlētāji desc


------------------------------------
-- 8. Pirkumi
-- visi pirkumi
SELECT * FROM Pirkums
-- Atlasa lietotāju pirkumus un pirkumu spēles un aprēķina pirkuma spēles atlaidi
SELECT
	Pirkums.*,
	Spēle.Nosaukums Spēle,
	PirkumaSpēle.Cena SpēlesCena,
	(Spēle.Cena - PirkumaSpēle.Cena) Atlaide
FROM Pirkums
LEFT JOIN PirkumaSpēle on PirkumaSpēle.PirkumsID = Pirkums.ID
LEFT JOIN Spēle on Spēle.ID = PirkumaSpēle.SpēleID
ORDER BY LietotājsID, Datums desc

-- Dokumentā 12.
-- Lietotāja pirkumu informācija, pirkumuskaits, nopirkto spēļu skaits, iztērētā summa un lielākais pirkums
SELECT
	LietotājsID,
	count(*) PirkumuSkaits,
	sum(SpēļuSkaits) SpēļuSkaits,
	sum(Cena) IztērētāSumma,
	max(Cena) LielākaisPirkums
FROM
	(
	SELECT
		Pirkums.ID,
		Pirkums.LietotājsID,
		Pirkums.Datums,
		PirkumaSpēle.Cena,
		count(*) SpēļuSkaits
	FROM Pirkums
	LEFT JOIN PirkumaSpēle on PirkumaSpēle.PirkumsID = Pirkums.ID
	GROUP BY Pirkums.ID, Pirkums.LietotājsID, Pirkums.Datums, PirkumaSpēle.Cena) sub
GROUP BY LietotājsID

-- Dokumentā 13.
-- Spēles ienākumi
SELECT
	Spēle.ID,
	Spēle.Nosaukums,
	sum(PirkumaSpēle.Cena) Ienākumi
FROM Spēle
LEFT JOIN PirkumaSpēle on PirkumaSpēle.SpēleID = Spēle.ID
GROUP BY Spēle.ID, Spēle.Nosaukums
ORDER BY Ienākumi desc
-- Izstrādātāja ienākumi
SELECT
	Izstrādātājs.Nosaukums,
	sum(PirkumaSpēle.Cena) Ienākumi
FROM Izstrādātājs
LEFT JOIN Spēle on Spēle.Izstrādātājs = Izstrādātājs.Nosaukums
LEFT JOIN PirkumaSpēle on PirkumaSpēle.SpēleID = Spēle.ID
GROUP BY Izstrādātājs.Nosaukums
ORDER BY Ienākumi desc
------------------------------------
-- 9. Vēlmju saraksts
SELECT * FROM VēlmjuSaraksts
-- lietotāja vēlmju saraksts sakārtots pēc lietotāja definētas secības
SELECT
	Lietotājs.ID,
	Lietotājs.Niks,
	VēlmjuSaraksts.Secība,
	Spēle.ID,
	Spēle.Nosaukums,
	VēlmjuSaraksts.PievienošanasDatums
FROM VēlmjuSaraksts
JOIN Lietotājs on Lietotājs.ID = VēlmjuSaraksts.LietotājsID
JOIN Spēle on Spēle.ID = VēlmjuSaraksts.SpēleID
ORDER BY Lietotājs.ID, VēlmjuSaraksts.Secība
-- cik vēlmju sarakstos ir spēle
SELECT
	Spēle.ID,
	Spēle.Nosaukums,
	count(VēlmjuSaraksts.LietotājsID) VēlmjuSarakstuSkaits
FROM Spēle
LEFT JOIN VēlmjuSaraksts on VēlmjuSaraksts.SpēleID = Spēle.ID
GROUP BY Spēle.ID, Spēle.Nosaukums
ORDER BY VēlmjuSarakstuSkaits desc

-------------------------------------
-- 10. Vērtējumi
-- Spēles recenzijas
SELECT Spēle.ID, Spēle.Nosaukums, Recenzija.*
FROM Spēle
LEFT JOIN Recenzija on Recenzija.SpēleID = Spēle.ID
ORDER BY Spēle.ID, Datums desc

-- katras spēles vidējais vērtējums
SELECT Spēle.ID, Spēle.Nosaukums, avg(Recenzija.Vērtējums) VidējaisVērtējums
FROM Spēle
left join Recenzija on Recenzija.SpēleID = Spēle.ID
group by Spēle.ID, Spēle.Nosaukums
order by VidējaisVērtējums desc

-- Lietotāja visas recenzijas
SELECT Lietotājs.ID, Lietotājs.Niks, Recenzija.*
FROM Lietotājs
LEFT JOIN Recenzija on Recenzija.LietotājsID = Lietotājs.ID
ORDER BY Lietotājs.ID, Recenzija.SpēleID

-- Dokumentā 14.
-- 10.1 žanra vislabāk novērtētā spēle
SELECT * FROM
	(
	SELECT -- saranko žanra spēles pēc vidējā vērtējuma
		ŽanrsNosaukums,
		svv.*,
		DENSE_RANK() over (partition by ŽanrsNosaukums ORDER BY VidējaisVērtējums desc) vieta -- rank pēc vidējā vērtējuma žanrā
	FROM
		( -- Spēles vidējais vērtējums
		SELECT Spēle.ID, Spēle.Nosaukums, avg(Recenzija.Vērtējums) VidējaisVērtējums
		FROM Spēle
		LEFT JOIN Recenzija on Recenzija.SpēleID = Spēle.ID
		GROUP BY Spēle.ID, Spēle.Nosaukums) svv -- spēļu vidējais vērtējums
	LEFT JOIN SpēleŽanrs sz on sz.SpēleID = svv.ID) ss -- spēļu žanri
WHERE ss.vieta = 1 -- žanra vislabāk novērtētā spēle

-- Lietotāja vislabāk novērtētā spēle
SELECT * FROM
	(
	SELECT
		Lietotājs.ID,
		Lietotājs.Niks,
		svv.*,
		DENSE_RANK() over (partition by Lietotājs.ID ORDER BY VidējaisVērtējums desc) vieta -- rank pēc vidējā vērtējuma lietotājam
	FROM
		(
		SELECT LietotājsID, avg(Recenzija.Vērtējums) VidējaisVērtējums
		FROM Recenzija
		GROUP BY LietotājsID) svv -- lietotāju vidējais vērtējums
	LEFT JOIN Lietotājs on Lietotājs.ID = svv.LietotājsID) ss -- lietotāji
WHERE ss.vieta = 1 -- lietotāja vislabāk novērtētā spēle


-- spēles vidējais vērtējums pret pelņu
SELECT
	Spēle.ID,
	Spēle.Nosaukums,
	avg(Recenzija.Vērtējums) VidējaisVērtējums,
	sum(PirkumaSpēle.Cena) Ienākumi
FROM Spēle
LEFT JOIN Recenzija on Recenzija.SpēleID = Spēle.ID
LEFT JOIN PirkumaSpēle on PirkumaSpēle.SpēleID = Spēle.ID
GROUP BY Spēle.ID, Spēle.Nosaukums
ORDER BY VidējaisVērtējums desc


--------------------
-- Sasniegumi

-- Lietotājs spēlējot spēles spēj nopelnīt sasniegumus(achievements) attiecīgajai spēlei.
-- Lietotāja sasniegumi
SELECT
	Lietotājs.ID,
	Lietotājs.Niks,
	Sasniegums.ID,
	Sasniegums.Nosaukums,
	Sasniegums.SpēleID,
	LietotājsSasniegums.Datums
FROM Lietotājs
LEFT JOIN LietotājsSasniegums on LietotājsSasniegums.LietotājsID = Lietotājs.ID
LEFT JOIN Sasniegums on Sasniegums.ID = LietotājsSasniegums.SasniegumsID
ORDER BY Lietotājs.ID, Sasniegums.SpēleID, Sasniegums.ID

-- cik sasniegumus sasniedzis spēlētājs, cik konkrētai spēlei
SELECT
	Lietotājs.ID,
	Lietotājs.Niks,
	Spēle.ID,
	Spēle.Nosaukums,
	count(Sasniegums.ID) SasniegumuSkaits
FROM Lietotājs
LEFT JOIN LietotājsSasniegums on LietotājsSasniegums.LietotājsID = Lietotājs.ID
LEFT JOIN Sasniegums on Sasniegums.ID = LietotājsSasniegums.SasniegumsID
LEFT JOIN Spēle on Spēle.ID = Sasniegums.SpēleID
GROUP BY Lietotājs.ID, Lietotājs.Niks, Spēle.ID, Spēle.Nosaukums
ORDER BY Lietotājs.ID, Spēle.ID
