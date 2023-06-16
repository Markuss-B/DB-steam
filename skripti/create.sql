CREATE TABLE Lietotājs (
	ID int IDENTITY(1000,1) PRIMARY KEY,
	Niks nvarchar(50) NOT NULL,
	Izveidots date DEFAULT getUTCDate()
);

CREATE TABLE Draudzējas (
	Lietotājs1 int NOT NULL FOREIGN KEY REFERENCES Lietotājs(ID),
	Lietotājs2 int NOT NULL FOREIGN KEY REFERENCES Lietotājs(ID),
	Datums date
	PRIMARY KEY (Lietotājs1, Lietotājs2)
);

CREATE TABLE Izstrādātājs (
	Nosaukums nvarchar(50) NOT NULL PRIMARY KEY,
	DibināšanasDatums date DEFAULT getUTCDate(),
	Apraksts nvarchar(MAX)
);

CREATE TABLE Izplatītājs (
	Nosaukums nvarchar(50) NOT NULL PRIMARY KEY,
	DibināšanasDatums date DEFAULT getUTCDate(),
	Apraksts nvarchar(MAX)
);

CREATE TABLE Spēle (
	ID int IDENTITY(1,1) PRIMARY KEY,
	Nosaukums nvarchar(100) NOT NULL,
	Versija nvarchar(50) DEFAULT '1.0.0',
	Cena smallmoney NOT NULL,
	Akcija int DEFAULT 0,
	IzdošanasDatums date DEFAULT getUTCDate(),
	Izstrādātājs nvarchar(50) NOT NULL FOREIGN KEY REFERENCES Izstrādātājs(Nosaukums),
	Izplatītājs nvarchar(50) NOT NULL FOREIGN KEY REFERENCES Izplatītājs(Nosaukums),
);

CREATE TABLE Žanrs (
	Nosaukums nvarchar(50) NOT NULL PRIMARY KEY,
	Apraksts nvarchar(MAX)
);

CREATE TABLE SpēleŽanrs (
	SpēleID int NOT NULL FOREIGN KEY REFERENCES Spēle(ID),
	ŽanrsNosaukums nvarchar(50) NOT NULL FOREIGN KEY REFERENCES Žanrs(Nosaukums),
	PRIMARY KEY (SpēleID, ŽanrsNosaukums)
);

CREATE TABLE LietotājsSpēle (
	LietotājsID int NOT NULL FOREIGN KEY REFERENCES Lietotājs(ID),
	SpēleID int NOT NULL FOREIGN KEY REFERENCES Spēle(ID),
	SpēlētāsStundas int DEFAULT 0,
	IegūšanasDatums date DEFAULT getUTCDate(),
	irIecienīta bit DEFAULT 0,
	InstalētāVersija nvarchar(50),
	PRIMARY KEY (LietotājsID, SpēleID)
);

CREATE TABLE LietotājaKategorija (
	ID int IDENTITY(1,1) PRIMARY KEY,
	LietotājsID int NOT NULL FOREIGN KEY REFERENCES Lietotājs(ID),
	Nosaukums nvarchar(50) NOT NULL,
	UNIQUE (LietotājsID, Nosaukums)
);

CREATE TABLE LietotājaKategorijaSpēle (
	LietotājsKategorijaID int NOT NULL FOREIGN KEY REFERENCES LietotājaKategorija(ID),
	SpēleID int NOT NULL FOREIGN KEY REFERENCES Spēle(ID),
	PRIMARY KEY (LietotājsKategorijaID, SpēleID)
);

CREATE TABLE VēlmjuSaraksts (
	LietotājsID int NOT NULL FOREIGN KEY REFERENCES Lietotājs(ID),
	SpēleID int NOT NULL FOREIGN KEY REFERENCES Spēle(ID),
	PievienošanasDatums smalldatetime DEFAULT getUTCDate(),
	Secība int NOT NULL,
	PRIMARY KEY (LietotājsID, SpēleID)
);

CREATE TABLE NorēķinuAdrese (
	ID int IDENTITY(1,1) PRIMARY KEY,
	Valsts nvarchar(50) NOT NULL,
	Pilsēta nvarchar(50) NOT NULL,
	Iela nvarchar(50) NOT NULL,
	MājasNr nvarchar(10) NOT NULL,
	DzīvokļaNr nvarchar(10) NOT NULL,
	PastaIndekss nvarchar(10) NOT NULL
);

CREATE TABLE Persona (
    ID int PRIMARY KEY FOREIGN KEY REFERENCES Lietotājs(ID),
    Vārds nvarchar(50) NOT NULL,
    Uzvārds nvarchar(50) NOT NULL,
    DzimšanasDatums date NOT NULL,
    EPasts nvarchar(100) NOT NULL UNIQUE,
    Parole nvarchar(100) NOT NULL,
	NorēķinuAdreseID int NOT NULL FOREIGN KEY REFERENCES NorēķinuAdrese(ID)
);

CREATE TABLE Pirkums (
	ID int IDENTITY(1,1) PRIMARY KEY,
	LietotājsID int NOT NULL FOREIGN KEY REFERENCES Lietotājs(ID),
	Datums smalldatetime DEFAULT getUTCDate(),
	Summa smallmoney NOT NULL
);

CREATE TABLE Maksājums (
	ID int IDENTITY(1,1) PRIMARY KEY,
	MaksājumaMetode nvarchar(50) NOT NULL,
	KartesCipari char(4),
	NorēķinuAdreseID int NOT NULL FOREIGN KEY REFERENCES NorēķinuAdrese(ID),
	PirkumsID int NOT NULL FOREIGN KEY REFERENCES Pirkums(ID)
);

CREATE TABLE PirkumaSpēle (
	PirkumsID int NOT NULL FOREIGN KEY REFERENCES Pirkums(ID),
	SpēleID int NOT NULL FOREIGN KEY REFERENCES Spēle(ID),
	Cena smallmoney NOT NULL,
	PRIMARY KEY (PirkumsID, SpēleID)
);

CREATE TABLE Recenzija (
	ID int IDENTITY(1,1) PRIMARY KEY,
	LietotājsID int NOT NULL FOREIGN KEY REFERENCES Lietotājs(ID),
	SpēleID int NOT NULL FOREIGN KEY REFERENCES Spēle(ID),
	Teksts nvarchar(MAX),
	Vērtējums int NOT NULL,
	Datums smalldatetime DEFAULT getUTCDate(),
	CONSTRAINT CK_Recenzija_Vērtējums CHECK (Vērtējums >= 1 AND Vērtējums <= 10),
	UNIQUE (LietotājsID, SpēleID)
);

CREATE TABLE Sasniegums (
	ID int IDENTITY(1,1) PRIMARY KEY,
	Nosaukums nvarchar(50) NOT NULL,
	Teksts nvarchar(255),
	SpēleID int NOT NULL FOREIGN KEY REFERENCES Spēle(ID)
);

CREATE TABLE LietotājsSasniegums (
	LietotājsID int NOT NULL FOREIGN KEY REFERENCES Lietotājs(ID),
	SasniegumsID int NOT NULL FOREIGN KEY REFERENCES Sasniegums(ID),
	Datums smalldatetime DEFAULT getUTCDate(),
	PRIMARY KEY (LietotājsID, SasniegumsID)
);

CREATE TABLE MantasKlase (
	ID int IDENTITY(1,1) PRIMARY KEY,
	Nosaukums nvarchar(50) NOT NULL,
	Apraksts nvarchar(255),
	SpēleID int NOT NULL FOREIGN KEY REFERENCES Spēle(ID),
	UNIQUE (SpēleID, Nosaukums)
);

CREATE TABLE Manta (
	ID int IDENTITY(1,1) PRIMARY KEY,
	ĪpašnieksID int NOT NULL FOREIGN KEY REFERENCES Lietotājs(ID),
	MantasKlaseID int NOT NULL FOREIGN KEY REFERENCES MantasKlase(ID),
	DotaisVārds nvarchar(50),
	IzveidesDatums smalldatetime NOT NULL DEFAULT getUTCDate() 
);

CREATE TABLE MantasĪpašniekuVēsture (
	LietotājsID int NOT NULL FOREIGN KEY REFERENCES Lietotājs(ID),
	MantaID int NOT NULL FOREIGN KEY REFERENCES Manta(ID),
	DatumsLīdz smalldatetime NOT NULL DEFAULT getUTCDate(),
	PRIMARY KEY (MantaID, LietotājsID)
);

CREATE TABLE Serveris (
    ID int IDENTITY(1,1) PRIMARY KEY,
    IPAddress nvarchar(15) NOT NULL,
    Port int NOT NULL,
    Nosaukums nvarchar(50) NOT NULL,
    SpēleID int NOT NULL FOREIGN KEY REFERENCES Spēle(ID),
    UNIQUE (IPAddress, Port)
);

CREATE TABLE LietotājsSpēlē (
	LietotājsID int PRIMARY KEY FOREIGN KEY REFERENCES Lietotājs(ID),
	SpēleID int NOT NULL FOREIGN KEY REFERENCES Spēle(ID),
	ServerisID int FOREIGN KEY REFERENCES Serveris(ID),
	Datums smalldatetime DEFAULT getUTCDate() 
);

CREATE TABLE Sarakste (
	ID int IDENTITY(1,1) PRIMARY KEY,
	Nosaukums nvarchar(50) NOT NULL,
	IzveidesDatums smalldatetime DEFAULT getUTCDate()
);

CREATE TABLE Ziņa (
	ID int IDENTITY(1,1) PRIMARY KEY,
	LietotājsID int NOT NULL FOREIGN KEY REFERENCES Lietotājs(ID),
	SaraksteID int NOT NULL FOREIGN KEY REFERENCES Sarakste(ID),
	Teksts nvarchar(MAX) NOT NULL,
	Datums smalldatetime DEFAULT getUTCDate()
);

CREATE TABLE SarakstesDalībnieks (
	LietotājsID int NOT NULL FOREIGN KEY REFERENCES Lietotājs(ID),
	SaraksteID int NOT NULL FOREIGN KEY REFERENCES Sarakste(ID),
	PievienošanāsDatums smalldatetime DEFAULT getUTCDate(),
	PēdējāLasītāZiņaID int FOREIGN KEY REFERENCES Ziņa(ID),
	PRIMARY KEY (LietotājsID, SaraksteID)
);

CREATE TABLE Grupa (
	ID int IDENTITY(1,1) PRIMARY KEY,
	Nosaukums nvarchar(50) NOT NULL,
	Apraksts nvarchar(255),
	IzveidesDatums smalldatetime DEFAULT getUTCDate(),
	SaraksteID int FOREIGN KEY REFERENCES Sarakste(ID)
);

CREATE TABLE Forums (
	ID int IDENTITY(1,1) PRIMARY KEY,
	Nosaukums nvarchar(50) NOT NULL,
	Apraksts nvarchar(255) NOT NULL,
	SpēleID int FOREIGN KEY REFERENCES Spēle(ID),
	GrupaID int FOREIGN KEY REFERENCES Grupa(ID)
);

CREATE TABLE Diskusija (
	ID int IDENTITY(1,1) PRIMARY KEY,
	Nosaukums nvarchar(50) NOT NULL,
	Teksts nvarchar(MAX) NOT NULL,
	ForumsID int NOT NULL FOREIGN KEY REFERENCES Forums(ID),
	IzveidotājsID int NOT NULL FOREIGN KEY REFERENCES Lietotājs(ID),
	Datums smalldatetime DEFAULT getUTCDate()
);

CREATE TABLE Komentārs (
	ID int IDENTITY(1,1) PRIMARY KEY,
	Teksts nvarchar(MAX) NOT NULL,
	DiskusijaID int NOT NULL FOREIGN KEY REFERENCES Diskusija(ID),
	LietotājsID int NOT NULL FOREIGN KEY REFERENCES Lietotājs(ID),
	Datums smalldatetime DEFAULT getUTCDate()
);