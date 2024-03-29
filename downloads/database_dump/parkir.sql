--
-- PostgreSQL database dump
--

-- Dumped from database version 14.5
-- Dumped by pg_dump version 14.5

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: gate; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.gate (
    id integer NOT NULL,
    no_pos character varying(10),
    tipe_pos character varying(30),
    jns_kendaraan character varying(50),
    ip_cam character varying(60)
);


ALTER TABLE public.gate OWNER TO postgres;

--
-- Name: gate_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.gate_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.gate_id_seq OWNER TO postgres;

--
-- Name: gate_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.gate_id_seq OWNED BY public.gate.id;


--
-- Name: karcis; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.karcis (
    id integer NOT NULL,
    barcode character varying(150),
    datetime timestamp(6) with time zone,
    gate character varying(20),
    images_path character varying(255),
    status_parkir boolean DEFAULT false NOT NULL,
    jenis_kendaraan character varying(100),
    ip_raspi character varying(15)
);


ALTER TABLE public.karcis OWNER TO postgres;

--
-- Name: karcis_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.karcis_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.karcis_id_seq OWNER TO postgres;

--
-- Name: karcis_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.karcis_id_seq OWNED BY public.karcis.id;


--
-- Name: kasir; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.kasir (
    id integer NOT NULL,
    nik character varying(100),
    nama character varying(80),
    hp character varying(15),
    alamat character varying(255),
    jm_masuk character varying(10),
    jm_keluar character varying(10),
    no_pos character varying(10)
);


ALTER TABLE public.kasir OWNER TO postgres;

--
-- Name: kasir_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.kasir_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.kasir_id_seq OWNER TO postgres;

--
-- Name: kasir_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.kasir_id_seq OWNED BY public.kasir.id;


--
-- Name: rfid; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rfid (
    id integer NOT NULL,
    rfid character varying(100),
    nama character varying(80)
);


ALTER TABLE public.rfid OWNER TO postgres;

--
-- Name: rfid_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.rfid_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.rfid_id_seq OWNER TO postgres;

--
-- Name: rfid_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.rfid_id_seq OWNED BY public.rfid.id;


--
-- Name: tarif; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tarif (
    id integer NOT NULL,
    no_pos character varying(10),
    tarif_perjam integer NOT NULL,
    tarif_per24jam integer NOT NULL,
    jns_kendaraan character varying(50)
);


ALTER TABLE public.tarif OWNER TO postgres;

--
-- Name: tarif_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tarif_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tarif_id_seq OWNER TO postgres;

--
-- Name: tarif_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tarif_id_seq OWNED BY public.tarif.id;


--
-- Name: tarif_tarif_per24jam_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tarif_tarif_per24jam_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tarif_tarif_per24jam_seq OWNER TO postgres;

--
-- Name: tarif_tarif_per24jam_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tarif_tarif_per24jam_seq OWNED BY public.tarif.tarif_per24jam;


--
-- Name: tarif_tarif_perjam_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tarif_tarif_perjam_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tarif_tarif_perjam_seq OWNER TO postgres;

--
-- Name: tarif_tarif_perjam_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tarif_tarif_perjam_seq OWNED BY public.tarif.tarif_perjam;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(100),
    user_level character varying(80),
    password character varying(255)
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: gate id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.gate ALTER COLUMN id SET DEFAULT nextval('public.gate_id_seq'::regclass);


--
-- Name: karcis id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.karcis ALTER COLUMN id SET DEFAULT nextval('public.karcis_id_seq'::regclass);


--
-- Name: kasir id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kasir ALTER COLUMN id SET DEFAULT nextval('public.kasir_id_seq'::regclass);


--
-- Name: rfid id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rfid ALTER COLUMN id SET DEFAULT nextval('public.rfid_id_seq'::regclass);


--
-- Name: tarif id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tarif ALTER COLUMN id SET DEFAULT nextval('public.tarif_id_seq'::regclass);


--
-- Name: tarif tarif_perjam; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tarif ALTER COLUMN tarif_perjam SET DEFAULT nextval('public.tarif_tarif_perjam_seq'::regclass);


--
-- Name: tarif tarif_per24jam; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tarif ALTER COLUMN tarif_per24jam SET DEFAULT nextval('public.tarif_tarif_per24jam_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: gate; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.gate (id, no_pos, tipe_pos, jns_kendaraan, ip_cam) FROM stdin;
1	1	masuk	motor	192.168.100.10#192.168.100.12
2	1	keluar	motor	192.168.100.16#192.168.100.18
3	3	Keluar	Mobil	192.168.100.7#192.168.100.8
5	12	Masuk	Motor	456456456
6	10	Masuk	Mobil	192.168.100.10#192.168.100.14
\.


--
-- Data for Name: karcis; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.karcis (id, barcode, datetime, gate, images_path, status_parkir, jenis_kendaraan, ip_raspi) FROM stdin;
44	6137730	2023-01-18 16:07:41+07	2	\N	t	mobil	192.168.100.82
42	6132545	2023-01-18 15:55:56+07	2	\N	t	mobil	192.168.100.82
45	47289	2023-01-22 07:03:01+07	2	\N	f	mobil	192.168.100.82
47	47429	2023-01-22 07:04:41+07	2	\N	f	mobil	192.168.100.82
48	47711	2023-01-22 07:07:23+07	2	\N	f	mobil	192.168.100.82
50	48741	2023-01-22 07:17:53+07	2	\N	f	mobil	192.168.100.82
51	48988	2023-01-22 07:20:00+07	2	\N	f	mobil	192.168.100.82
52	49012	2023-01-22 07:20:24+07	2	\N	f	mobil	192.168.100.82
53	49099	2023-01-22 07:21:11+07	2	\N	f	mobil	192.168.100.82
54	49323	2023-01-22 07:23:35+07	2	\N	f	mobil	192.168.100.82
55	49400	2023-01-22 07:24:12+07	2	\N	f	mobil	192.168.100.82
56	49828	2023-01-22 07:28:40+07	2	\N	f	mobil	192.168.100.82
58	51241	2023-01-22 07:42:53+07	2	\N	f	mobil	192.168.100.82
59	51317	2023-01-22 07:43:29+07	2	\N	f	mobil	192.168.100.82
60	51422	2023-01-22 07:44:34+07	2	\N	f	mobil	192.168.100.82
61	52199	2023-01-22 07:52:11+07	2	\N	f	mobil	192.168.100.82
62	52311	2023-01-22 07:53:23+07	2	\N	f	mobil	192.168.100.82
63	52406	2023-01-22 07:54:18+07	2	\N	f	mobil	192.168.100.82
64	52442	2023-01-22 07:54:54+07	2	\N	f	mobil	192.168.100.82
65	52714	2023-01-22 07:57:26+07	2	\N	f	mobil	192.168.100.82
66	52833	2023-01-22 07:58:45+07	2	\N	f	mobil	192.168.100.82
67	52894	2023-01-22 07:59:06+07	2	\N	f	mobil	192.168.100.82
68	57204	2023-01-22 08:02:16+07	2	\N	f	mobil	192.168.100.82
69	57224	2023-01-22 08:02:36+07	2	\N	f	mobil	192.168.100.82
72	78117	2023-01-22 10:11:29+07	2	\N	f	mobil	192.168.100.82
57	49896	2023-01-22 07:29:08+07	2	\N	t	mobil	192.168.100.82
49	48011	2023-01-22 07:10:23+07	2	\N	t	mobil	192.168.100.82
46	47405	2023-01-22 07:04:17+07	2	\N	t	mobil	192.168.100.82
71	78094	2023-01-22 10:11:06+07	2	\N	t	mobil	192.168.100.82
70	78005	2023-01-22 10:10:17+07	2	\N	t	mobil	192.168.100.82
73	198913	2023-01-22 22:19:25+07	2	\N	f	mobil	192.168.100.82
41	6100104	2023-01-18 12:31:15+07	2	\N	t	mobil	192.168.100.82
43	6132804	2023-01-18 15:58:15+07	2	\N	t	mobil	192.168.100.82
\.


--
-- Data for Name: kasir; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.kasir (id, nik, nama, hp, alamat, jm_masuk, jm_keluar, no_pos) FROM stdin;
1	111223344	susi	085263636	darussalam	08:00	12:00	1
2	1144523344	budi	0852636234	darussalam	12:00	18:00	1
\.


--
-- Data for Name: rfid; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.rfid (id, rfid, nama) FROM stdin;
1	0014832825	razi
6	123123123	sdfsdf
10	123	sasdfdsf
11	213123123	sdfsdfsdf
14	11233	sdfsdfsdf
15	11111111111	sdfsdf
16	123123123	sadfsdfsd
17	111	sdfsdfsdf
18	22222	sfdsdf
19	123123	sdfsdf
20	121123	sdfsdfsd
21	123123	sdfsdfsd
23	34323423	dfgdf
24	12312	sfdsdf
26	123	sdfsdf
27	123123	sdfsdfs
28	24234	nfgjhg
30	1111111	sanusi
5	14323423	anto
13	1231	santi
\.


--
-- Data for Name: tarif; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tarif (id, no_pos, tarif_perjam, tarif_per24jam, jns_kendaraan) FROM stdin;
7	\N	1000	8000	motor
8	\N	2000	16000	mobil
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, username, user_level, password) FROM stdin;
2	susi	Kasir	123
1	andi	admin	123
\.


--
-- Name: gate_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.gate_id_seq', 6, true);


--
-- Name: karcis_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.karcis_id_seq', 73, true);


--
-- Name: kasir_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.kasir_id_seq', 2, true);


--
-- Name: rfid_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.rfid_id_seq', 30, true);


--
-- Name: tarif_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tarif_id_seq', 8, true);


--
-- Name: tarif_tarif_per24jam_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tarif_tarif_per24jam_seq', 1, false);


--
-- Name: tarif_tarif_perjam_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tarif_tarif_perjam_seq', 1, false);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 4, true);


--
-- Name: gate gate_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.gate
    ADD CONSTRAINT gate_pkey PRIMARY KEY (id);


--
-- Name: karcis karcis_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.karcis
    ADD CONSTRAINT karcis_pkey PRIMARY KEY (id);


--
-- Name: kasir kasir_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kasir
    ADD CONSTRAINT kasir_pkey PRIMARY KEY (id);


--
-- Name: rfid rfid_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rfid
    ADD CONSTRAINT rfid_pkey PRIMARY KEY (id);


--
-- Name: tarif tarif_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tarif
    ADD CONSTRAINT tarif_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

