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
-- Name: clients_socket; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.clients_socket (
    id integer NOT NULL,
    ip character varying(20) NOT NULL,
    port integer NOT NULL
);


ALTER TABLE public.clients_socket OWNER TO postgres;

--
-- Name: clients_socket_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.clients_socket_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.clients_socket_id_seq OWNER TO postgres;

--
-- Name: clients_socket_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.clients_socket_id_seq OWNED BY public.clients_socket.id;


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
    datetime timestamp without time zone,
    gate character varying(20),
    images_path character varying(255),
    status_parkir boolean DEFAULT false NOT NULL,
    jenis_kendaraan character varying(30),
    ip_raspi character varying(25),
    date_keluar timestamp without time zone,
    lama_parkir interval,
    tarif integer,
    nopol character varying(60),
    kd_shift character varying(20),
    jns_transaksi character varying(60),
    images_path_keluar character varying(255),
    lost_ticket boolean DEFAULT false NOT NULL
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
-- Name: laporan_users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.laporan_users (
    id integer NOT NULL,
    barcode character varying(30),
    ket character varying(255)
);


ALTER TABLE public.laporan_users OWNER TO postgres;

--
-- Name: laporan_users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.laporan_users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.laporan_users_id_seq OWNER TO postgres;

--
-- Name: laporan_users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.laporan_users_id_seq OWNED BY public.laporan_users.id;


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
    rules text DEFAULT ''::text,
    jns_kendaraan character varying(50),
    toleransi integer,
    tipe_tarif character varying(20),
    base_rules text,
    denda integer DEFAULT 0
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
-- Name: tes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tes (
    id integer NOT NULL,
    barcode character varying(150),
    datetime timestamp(6) with time zone,
    gate character varying(20),
    images_path character varying(255),
    jns_kendaraan character varying(20)
);


ALTER TABLE public.tes OWNER TO postgres;

--
-- Name: tes_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tes_id_seq OWNER TO postgres;

--
-- Name: tes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tes_id_seq OWNED BY public.tes.id;


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
-- Name: voucher; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.voucher (
    id integer NOT NULL,
    id_pel character varying(30),
    lokasi character varying(255),
    tarif integer NOT NULL,
    masa_berlaku date,
    jns_kendaraan character varying(20)
);


ALTER TABLE public.voucher OWNER TO postgres;

--
-- Name: voucher_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.voucher_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.voucher_id_seq OWNER TO postgres;

--
-- Name: voucher_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.voucher_id_seq OWNED BY public.voucher.id;


--
-- Name: voucher_tarif_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.voucher_tarif_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.voucher_tarif_seq OWNER TO postgres;

--
-- Name: voucher_tarif_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.voucher_tarif_seq OWNED BY public.voucher.tarif;


--
-- Name: clients_socket id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clients_socket ALTER COLUMN id SET DEFAULT nextval('public.clients_socket_id_seq'::regclass);


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
-- Name: laporan_users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.laporan_users ALTER COLUMN id SET DEFAULT nextval('public.laporan_users_id_seq'::regclass);


--
-- Name: rfid id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rfid ALTER COLUMN id SET DEFAULT nextval('public.rfid_id_seq'::regclass);


--
-- Name: tarif id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tarif ALTER COLUMN id SET DEFAULT nextval('public.tarif_id_seq'::regclass);


--
-- Name: tes id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tes ALTER COLUMN id SET DEFAULT nextval('public.tes_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Name: voucher id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.voucher ALTER COLUMN id SET DEFAULT nextval('public.voucher_id_seq'::regclass);


--
-- Name: voucher tarif; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.voucher ALTER COLUMN tarif SET DEFAULT nextval('public.voucher_tarif_seq'::regclass);


--
-- Data for Name: clients_socket; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.clients_socket (id, ip, port) FROM stdin;
\.


--
-- Data for Name: gate; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.gate (id, no_pos, tipe_pos, jns_kendaraan, ip_cam) FROM stdin;
1	1	masuk	motor	192.168.100.10#192.168.100.12
2	1	keluar	motor	192.168.100.16#192.168.100.18
\.


--
-- Data for Name: karcis; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.karcis (id, barcode, datetime, gate, images_path, status_parkir, jenis_kendaraan, ip_raspi, date_keluar, lama_parkir, tarif, nopol, kd_shift, jns_transaksi, images_path_keluar, lost_ticket) FROM stdin;
11	50660908	2023-02-06 08:49:02	2	\N	t	mobil	192.168.100.82	2023-02-06 08:50:02	00:00:00	0	\N	\N	voucher	\N	f
6	3152785	2023-02-05 17:58:05	2	\N	t	mobil	192.168.100.82	2023-02-05 18:20:05	00:00:00	0	BL 1123	s1	casual	\N	f
7	3157001	2023-02-05 18:00:21	2	\N	t	mobil	192.168.100.82	2023-02-05 18:50:21	00:00:00	0	BL 1123	s1	casual	\N	f
10	4060904	2023-02-06 08:39:24	2	\N	f	mobil	192.168.100.82	\N	00:00:00	0	\N	\N	casual	\N	f
13	4070235	2023-02-06 09:32:55	2	\N	f	mobil	192.168.100.82	\N	00:00:00	0	\N	\N	casual	\N	f
14	4070312	2023-02-06 09:33:32	2	\N	f	mobil	192.168.100.82	\N	00:00:00	0	\N	\N	casual	\N	f
15	4070416	2023-02-06 09:34:36	2	\N	f	mobil	192.168.100.82	\N	00:00:00	0	\N	\N	casual	\N	f
18	4077300	2023-02-06 10:03:20	2	\N	f	mobil	192.168.100.82	\N	00:00:00	0	\N	\N	casual	\N	f
19	4077682	2023-02-06 10:07:02	2	\N	f	mobil	192.168.100.82	\N	00:00:00	0	\N	\N	casual	\N	f
20	4077682	2023-02-06 10:07:02	2	\N	f	mobil	192.168.100.82	\N	00:00:00	0	\N	\N	casual	\N	f
21	4077801	2023-02-06 10:08:21	2	\N	f	mobil	192.168.100.82	\N	00:00:00	0	\N	\N	casual	\N	f
22	4077817	2023-02-06 10:08:37	2	\N	f	mobil	192.168.100.82	\N	00:00:00	0	\N	\N	casual	\N	f
23	4077926	2023-02-06 10:09:46	2	\N	f	mobil	192.168.100.82	\N	00:00:00	0	\N	\N	casual	\N	f
24	4077927	2023-02-06 10:09:47	2	\N	f	mobil	192.168.100.82	\N	00:00:00	0	\N	\N	casual	\N	f
25	4091933	2023-02-06 11:49:53	2	\N	f	mobil	192.168.100.82	\N	00:00:00	0	\N	\N	casual	\N	f
26	4091996	2023-02-06 11:50:16	2	\N	f	mobil	192.168.100.82	\N	00:00:00	0	\N	\N	casual	\N	f
27	4097126	2023-02-06 12:01:46	2	\N	f	mobil	192.168.100.82	\N	00:00:00	0	\N	\N	casual	\N	f
28	4097127	2023-02-06 12:01:47	2	\N	f	mobil	192.168.100.82	\N	00:00:00	0	\N	\N	casual	\N	f
55	000	\N	\N	\N	t	Mobil	\N	2023-02-05 15:02:12	\N	20000	BL 3345	\N	casual	\N	t
16	4077102	2023-05-07 11:30:00	2	\N	f	mobil	192.168.100.82	\N	00:00:00	0	\N	\N	casual	\N	f
1	3127192	2023-02-05 15:02:12	2	\N	t	mobil	\N	2023-02-05 15:20:12	1 day 02:00:00	4000	BL 1123	s1	casual	\N	f
2	3132319	2023-02-05 15:53:39	2	\N	t	mobil	192.168.100.82	2023-03-05 15:53:39	01:00:00	4000	BL 1123	s1	casual	\N	f
3	3132399	2023-02-05 15:54:19	2	\N	t	mobil	192.168.100.82	2023-02-05 15:59:00	00:20:00	4000	BL 1123	s1	casual	\N	f
4	3132724	2023-02-05 15:57:44	2	\N	t	mobil	192.168.100.82	2023-02-05 17:57:44	02:05:00	4000	BL 1123	s1	casual	\N	f
5	3151621	2023-02-05 17:46:41	2	\N	t	mobil	192.168.100.82	2023-02-05 18:00:41	00:05:00	4000	BL 1123	s1	casual	\N	f
8	3158385	2023-02-05 18:14:05	2	\N	t	mobil	192.168.100.82	\N	00:00:00	0	\N	\N	casual	\N	f
29	4101693	2023-02-06 12:47:13	2	\N	f	mobil	192.168.100.82	\N	00:00:00	0	\N	\N	casual	\N	f
30	4101693	2023-02-06 12:47:13	2	\N	f	mobil	192.168.100.82	\N	00:00:00	0	\N	\N	casual	\N	f
31	4101790	2023-02-06 12:48:10	2	\N	t	mobil	192.168.100.82	\N	00:00:00	0	\N	\N	casual	\N	f
32	61992	2023-02-12 08:50:13	2	\N	t	mobil	192.168.100.82	\N	00:00:00	0	\N	\N	casual	\N	f
33	77835	2023-02-12 10:08:56	2	\N	f	mobil	192.168.100.82	\N	00:00:00	0	\N	\N	casual	\N	f
34	78325	2023-02-12 10:13:46	2	\N	f	mobil	192.168.100.82	\N	00:00:00	0	\N	\N	casual	\N	f
35	78516	2023-02-12 10:15:37	2	\N	f	mobil	192.168.100.82	\N	00:00:00	0	\N	\N	casual	\N	f
36	81423	2023-02-12 10:44:44	2	\N	f	mobil	192.168.100.82	\N	00:00:00	0	\N	\N	casual	\N	f
37	81423	2023-02-12 10:44:44	2	\N	f	mobil	192.168.100.82	\N	00:00:00	0	\N	\N	casual	\N	f
38	81491	2023-02-12 10:45:12	2	\N	t	mobil	192.168.100.82	\N	00:00:00	0	\N	\N	casual	\N	f
39	4168100	2023-02-16 19:11:21	2	\N	f	Mobil	192.168.100.82	\N	00:00:00	0	\N	\N	casual	\N	f
40	4168506	2023-02-16 19:15:27	2	\N	f	Mobil	192.168.100.82	\N	00:00:00	0	\N	\N	casual	\N	f
42	4169602	2023-02-16 19:26:23	2	\N	f	Mobil	192.168.100.82	\N	00:00:00	0	\N	\N	casual	\N	f
41	4168587	2023-02-16 19:16:08	2	\N	t	Mobil	192.168.100.82	\N	00:00:00	0	\N	\N	casual	\N	f
12	4070085	2023-02-06 09:31:05	2	\N	t	mobil	192.168.100.82	\N	00:00:00	0	\N	\N	casual	\N	f
43	4170936	2023-02-16 19:39:57	2	\N	f	Mobil	192.168.100.82	\N	00:00:00	0	\N	\N	casual	\N	f
44	4191828	2023-02-16 21:48:49	2	\N	f	Mobil	192.168.100.82	\N	00:00:00	0	\N	\N	casual	\N	f
45	4191829	2023-02-16 21:48:50	2	\N	f	Mobil	192.168.100.82	\N	00:00:00	0	\N	\N	casual	\N	f
46	4192179	2023-02-16 21:52:00	2	\N	f	Mobil	192.168.100.82	\N	00:00:00	0	\N	\N	casual	\N	f
47	4192285	2023-02-16 21:53:06	2	\N	t	Mobil	192.168.100.82	\N	00:00:00	0	\N	\N	casual	\N	f
17	4077103	2023-02-06 10:01:23	2	\N	t	mobil	192.168.100.82	\N	00:00:00	0	\N	\N	casual	\N	f
48	5089332	2023-02-27 11:23:54	2	\N	f	Mobil	192.168.100.82	\N	00:00:00	0	\N	\N	casual	\N	f
49	5089806	2023-02-27 11:28:28	2	\N	f	Mobil	192.168.100.82	\N	00:00:00	0	\N	\N	casual	\N	f
50	5089915	2023-02-27 11:29:37	2	\N	f	Mobil	192.168.100.82	\N	00:00:00	0	\N	\N	casual	\N	f
52	5097916	2023-02-27 12:09:38	2	\N	f	Mobil	192.168.100.82	\N	00:00:00	0	\N	\N	casual	\N	f
51	5090021	2023-02-27 11:30:43	2	\N	f	Mobil	192.168.100.82	\N	00:00:00	50000	\N	\N	casual	\N	f
\.


--
-- Data for Name: kasir; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.kasir (id, nik, nama, hp, alamat, jm_masuk, jm_keluar, no_pos) FROM stdin;
1	111223344	susi	085263636	darussalam	08:00	12:00	1
2	1144523344	budi	0852636234	darussalam	12:00	18:00	1
3	1234	abc	0853	cfg	12	13	1
4	1323	asda					
5	123123	doni	234234	fgdhfgh	12	123	34
\.


--
-- Data for Name: laporan_users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.laporan_users (id, barcode, ket) FROM stdin;
\.


--
-- Data for Name: rfid; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.rfid (id, rfid, nama) FROM stdin;
9	4323432	bwahahah
10	11111111111	asdasd
11	1312984732	sdlfklsdlkdsf
12	2093840932	sdndsvdv
7	0014832825	razi
13	5567	santi
14	102021	andri
4	1123123	antos
15	4323432	bwahahah
24	12312312	ssdfdsf
25	1123333333	susan
26	1123123	budianto
27	santi	123123
28	1	a
29	123	abc
\.


--
-- Data for Name: tarif; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tarif (id, rules, jns_kendaraan, toleransi, tipe_tarif, base_rules, denda) FROM stdin;
1	{"2": "1000", "6": "1000", "12": "1000", "18": "1000", "24": "5000"}	motor	10	other	{"2":"1000","4":"1000","6":"1000","24":"5000"}	20000
2	{"2": "2000", "6": "1000", "12": "1000", "18": "1000", "24": "6000"}	mobil	10	other	{"2":"2000","4":"1000","6":"1000","24":"6000"}	30000
49	{"2": "4000", "6": "3000", "12": "3000", "18": "3000", "24": "8000"}	Truck	10	other	{"2":"4000","4":"3000","6":"3000","24":"8000"}	6000
\.


--
-- Data for Name: tes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tes (id, barcode, datetime, gate, images_path, jns_kendaraan) FROM stdin;
1	12313123	2023-02-05 15:02:12+07	1	\N	motor
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, username, user_level, password) FROM stdin;
3	budi	kasir	1256
1	andi	Admin	admin
5	abc	Kasir	123
6	qwe	Admin	12345
2	susi	kasir	123
\.


--
-- Data for Name: voucher; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.voucher (id, id_pel, lokasi, tarif, masa_berlaku, jns_kendaraan) FROM stdin;
1	1123	svdsv	123123	2023-02-05	Motor
2	1123	RS Cempaka	15000	2023-02-05	Motor
3	1123	RS Cempaka	15000	2023-02-09	Motor
6	1123	RS Cempaka Lima	15000	2023-02-05	Motor
7	123456789019231248932	sdsdfdsfsssssssssssssssssdvsdv	1000000	2023-04-13	Motor
8	12345	RS	10000	2000-01-01	Motor
9	11231	cempaka lima	30000	2023-04-06	Motor
\.


--
-- Name: clients_socket_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.clients_socket_id_seq', 44, true);


--
-- Name: gate_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.gate_id_seq', 2, true);


--
-- Name: karcis_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.karcis_id_seq', 55, true);


--
-- Name: kasir_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.kasir_id_seq', 5, true);


--
-- Name: laporan_users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.laporan_users_id_seq', 1, false);


--
-- Name: rfid_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.rfid_id_seq', 29, true);


--
-- Name: tarif_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tarif_id_seq', 49, true);


--
-- Name: tes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tes_id_seq', 1, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 6, true);


--
-- Name: voucher_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.voucher_id_seq', 9, true);


--
-- Name: voucher_tarif_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.voucher_tarif_seq', 1, false);


--
-- Name: clients_socket clients_socket_ip_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clients_socket
    ADD CONSTRAINT clients_socket_ip_key UNIQUE (ip);


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
-- Name: laporan_users laporan_users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.laporan_users
    ADD CONSTRAINT laporan_users_pkey PRIMARY KEY (id);


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
-- Name: tes tes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tes
    ADD CONSTRAINT tes_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: voucher voucher_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.voucher
    ADD CONSTRAINT voucher_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

