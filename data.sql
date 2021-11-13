CREATE TABLE public._routes (
    id smallint,
    name character varying(15) DEFAULT NULL::character varying,
    grade character varying(3) DEFAULT NULL::character varying,
    spot character varying(13) DEFAULT NULL::character varying
);


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

