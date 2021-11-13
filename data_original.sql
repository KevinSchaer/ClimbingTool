--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.10
-- Dumped by pg_dump version 9.6.10

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: _routes; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._routes (
    id smallint,
    name character varying(15) DEFAULT NULL::character varying,
    grade character varying(3) DEFAULT NULL::character varying,
    spot character varying(13) DEFAULT NULL::character varying
);


ALTER TABLE public._routes OWNER TO rebasedata;

--
-- Name: _user_route; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._user_route (
    user_id smallint,
    route_id smallint,
    top_reached character varying(3) DEFAULT NULL::character varying,
    attempts smallint,
    score smallint,
    user_grade character varying(3) DEFAULT NULL::character varying,
    comment character varying(27) DEFAULT NULL::character varying,
    "time" character varying(19) DEFAULT NULL::character varying
);


ALTER TABLE public._user_route OWNER TO rebasedata;

--
-- Name: _users; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._users (
    id smallint,
    username character varying(8) DEFAULT NULL::character varying,
    hash character varying(102) DEFAULT NULL::character varying,
    bodyweight numeric(3,1) DEFAULT NULL::numeric,
    height smallint,
    age smallint,
    redpoint character varying(3) DEFAULT NULL::character varying,
    onsight character varying(2) DEFAULT NULL::character varying,
    about_me character varying(61) DEFAULT NULL::character varying,
    profile character varying(11) DEFAULT NULL::character varying
);


ALTER TABLE public._users OWNER TO rebasedata;

--
-- Data for Name: _routes; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._routes (id, name, grade, spot) FROM stdin;
1	Tschortschi 1	6b	Eppenberg
2	Biancogrötli	5a	Eppenberg
3	Kante	6a	Klus-Balsthal
4	Schulterriss	6a	Pelzli
5	Pitchounette	5c	Gueberschwihr
6	Lamiak de droit	5c	Gueberschwihr
7	Sensitive	6b+	Schartenflue
8	Pille-Palle	4a	Albbruck
9	Tabaluga	4a	Albbruck
10	Treppe	4c	Klus-Balsthal
11	Baluu	6c	Gempen
\.


--
-- Data for Name: _user_route; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._user_route (user_id, route_id, top_reached, attempts, score, user_grade, comment, "time") FROM stdin;
2	1	No	3	3	6b	not very special	2021-08-06 09:30:04
2	2	Yes	1	3	4c	easy peasy	2021-08-06 09:31:59
2	3	Yes	3	4	6a	nice one	2021-08-06 09:35:34
2	4	Yes	4	3	6a+	slippery	2021-08-06 09:37:14
1	5	Yes	3	3	5c+	hard moves	2021-08-06 09:39:42
1	6	Yes	1	4	5c+	badly positioned quickdraws	2021-08-06 09:41:16
1	1	No	4	3	6b	lots of dirt and sand	2021-08-06 09:42:17
1	7	Yes	3	3	6b+	nice pockets	2021-08-06 09:43:23
3	8	Yes	15	3	4b	very very hard route	2021-08-06 09:48:57
3	9	Yes	6	4	4a	fly high	2021-08-06 09:49:40
3	10	Yes	21	4	5a	not really like stairs :(	2021-08-06 09:50:48
1	11	Yes	11	5	6c+	tough but awesome!!	CURRENT_TIMESTAMP
\.


--
-- Data for Name: _users; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._users (id, username, hash, bodyweight, height, age, redpoint, onsight, about_me, profile) FROM stdin;
1	Philippe	pbkdf2:sha256:260000$Rqri13fuPaGoknNA$ff1ec1cb938cbf6016b5650deaca16bf549a7f8d4a9a97083540e23592384aa0	68.0	176	31	6b	5c	Famous Huusmaa from Basel!	1.jpg
2	Kevin	pbkdf2:sha256:260000$KzBnxDhPm2yX3Za7$c544675832e2451084c7a011f67f66e3e481b8bd2dde1d92dbfff11fadc586e2	74.5	183	28	6a+	5c	I am a little bit stronger than Huusmaa!	2.jpeg
3	Gill3r	pbkdf2:sha256:260000$vbpqJFdgu2laCGhM$a6ed84a193afb5272119502d1401755fea9078d25e5079868bf1cbd1760275b9	68.0	169	27	5b	5a	Unfortunately a little bit weaker than Kevin and Philippe! :(	default.png
\.


--
-- PostgreSQL database dump complete
--

