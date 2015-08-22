--
-- PostgreSQL database dump
--

-- Dumped from database version 9.3.4
-- Dumped by pg_dump version 9.3.4
-- Started on 2014-06-24 16:06:31 CST

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- TOC entry 175 (class 3079 OID 12670)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- TOC entry 2888 (class 0 OID 0)
-- Dependencies: 175
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

--
-- TOC entry 188 (class 1255 OID 44313)
-- Name: backup_node_tasks(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION backup_node_tasks() RETURNS trigger
    LANGUAGE plpgsql
    AS $$BEGIN 
   insert into node_tasks0 select * from node_tasks where id = OLD.id;
   RETURN OLD;
END;
$$;


ALTER FUNCTION public.backup_node_tasks() OWNER TO postgres;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 170 (class 1259 OID 44233)
-- Name: node_tasks; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE node_tasks (
    id integer NOT NULL,
    taskid character varying(50),
    taskinfo character varying,
    node character varying(50),
    state integer,
    times integer DEFAULT 0,
    level integer DEFAULT 0,
    atime timestamp without time zone,
    ctime timestamp without time zone,
    stime timestamp without time zone,
    ftime timestamp without time zone
);


ALTER TABLE public.node_tasks OWNER TO postgres;

--
-- TOC entry 173 (class 1259 OID 44269)
-- Name: node_tasks0; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE node_tasks0 (
    id integer NOT NULL,
    taskid character varying(50),
    taskinfo character varying,
    node character varying(50),
    state integer,
    times integer DEFAULT 0,
    level integer DEFAULT 0,
    atime timestamp without time zone,
    ctime timestamp without time zone,
    stime timestamp without time zone,
    ftime timestamp without time zone
);


ALTER TABLE public.node_tasks0 OWNER TO postgres;

--
-- TOC entry 172 (class 1259 OID 44242)
-- Name: node_tasks_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE node_tasks_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.node_tasks_id_seq OWNER TO postgres;

--
-- TOC entry 2889 (class 0 OID 0)
-- Dependencies: 172
-- Name: node_tasks_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE node_tasks_id_seq OWNED BY node_tasks.id;


--
-- TOC entry 171 (class 1259 OID 44239)
-- Name: task_logs; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE task_logs (
    id integer NOT NULL,
    taskid character varying(50),
    output character varying,
    errput character varying,
    ctime timestamp without time zone
);


ALTER TABLE public.task_logs OWNER TO postgres;

--
-- TOC entry 174 (class 1259 OID 44281)
-- Name: task_logs_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE task_logs_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.task_logs_id_seq OWNER TO postgres;

--
-- TOC entry 2890 (class 0 OID 0)
-- Dependencies: 174
-- Name: task_logs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE task_logs_id_seq OWNED BY task_logs.id;


--
-- TOC entry 2756 (class 2604 OID 44244)
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY node_tasks ALTER COLUMN id SET DEFAULT nextval('node_tasks_id_seq'::regclass);


--
-- TOC entry 2759 (class 2604 OID 44283)
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY task_logs ALTER COLUMN id SET DEFAULT nextval('task_logs_id_seq'::regclass);


--
-- TOC entry 2770 (class 2606 OID 44278)
-- Name: node_tasks0_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY node_tasks0
    ADD CONSTRAINT node_tasks0_pkey PRIMARY KEY (id);


--
-- TOC entry 2763 (class 2606 OID 44267)
-- Name: node_tasks_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY node_tasks
    ADD CONSTRAINT node_tasks_pkey PRIMARY KEY (id);


--
-- TOC entry 2767 (class 2606 OID 44292)
-- Name: task_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY task_logs
    ADD CONSTRAINT task_logs_pkey PRIMARY KEY (id);


--
-- TOC entry 2771 (class 1259 OID 44279)
-- Name: node_tasks0_state_idx; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX node_tasks0_state_idx ON node_tasks0 USING btree (state);


--
-- TOC entry 2772 (class 1259 OID 44280)
-- Name: node_tasks0_taskid_idx; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX node_tasks0_taskid_idx ON node_tasks0 USING btree (taskid);


--
-- TOC entry 2764 (class 1259 OID 44265)
-- Name: node_tasks_state_idx; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX node_tasks_state_idx ON node_tasks USING btree (state);


--
-- TOC entry 2765 (class 1259 OID 44268)
-- Name: node_tasks_taskid_idx; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX node_tasks_taskid_idx ON node_tasks USING btree (taskid);


--
-- TOC entry 2768 (class 1259 OID 44290)
-- Name: task_logs_taskid_idx; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX task_logs_taskid_idx ON task_logs USING btree (taskid);


--
-- TOC entry 2773 (class 2620 OID 44314)
-- Name: backup_node_tasks; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER backup_node_tasks BEFORE DELETE ON node_tasks FOR EACH ROW EXECUTE PROCEDURE backup_node_tasks();


--
-- TOC entry 2887 (class 0 OID 0)
-- Dependencies: 5
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


-- Completed on 2014-06-24 16:06:32 CST

--
-- PostgreSQL database dump complete
--

