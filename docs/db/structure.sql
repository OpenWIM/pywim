--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

SET search_path = wim, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

CREATE TABLE acquisition (
    id integer NOT NULL,
    date_time timestamp without time zone DEFAULT (now())::timestamp without time zone NOT NULL,
    vehicle_image bytea,
    temperature double precision,
    number_of_axles integer,
    axles_on_group_1 integer,
    axles_on_group_2 integer,
    axles_on_group_3 integer,
    axles_on_group_4 integer,
    axles_on_group_5 integer,
    axles_on_group_6 integer,
    axles_on_group_7 integer,
    axles_on_group_8 integer,
    axles_on_group_9 integer,
    speed double precision,
    gross_weight double precision,
    weight_axle_1 double precision,
    weight_axle_2 double precision,
    weight_axle_3 double precision,
    weight_axle_4 double precision,
    weight_axle_5 double precision,
    weight_axle_6 double precision,
    weight_axle_7 double precision,
    weight_axle_8 double precision,
    weight_axle_9 double precision,
    weight_axle_group_1 double precision,
    weight_axle_group_2 double precision,
    weight_axle_group_3 double precision,
    weight_axle_group_4 double precision,
    weight_axle_group_5 double precision,
    weight_axle_group_6 double precision,
    weight_axle_group_7 double precision,
    distance_axles_1_2 double precision,
    distance_axles_2_3 double precision,
    distance_axles_3_4 double precision,
    distance_axles_4_5 double precision,
    distance_axles_5_6 double precision,
    distance_axles_6_7 double precision,
    distance_axles_7_8 double precision,
    distance_axles_8_9 double precision,
    license_plate character varying(7),
    acquisition_mode smallint DEFAULT 0,
    valid_segmentation boolean DEFAULT true,
    status boolean DEFAULT true
);


CREATE TABLE acquisition_data(
    acquisition integer NOT NULL,
    time_seconds double precision,
    sensor1 double precision,
    sensor2 double precision,
    sensor3 double precision,
    sensor4 double precision,
    sensor5 double precision,
    sensor6 double precision,
    sensor7 double precision,
    sensor8 double precision,
    inductive_loop integer
);


CREATE SEQUENCE acquisition_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE acquisition_id_seq OWNED BY acquisition.id;

CREATE TABLE acquisition_sensor_weigh (
    acquisition integer NOT NULL,
    num_sensor integer NOT NULL,
    axles integer,
    axles_on_group_1 integer,
    axles_on_group_2 integer,
    axles_on_group_3 integer,
    axles_on_group_4 integer,
    axles_on_group_5 integer,
    axles_on_group_6 integer,
    axles_on_group_7 integer,
    axles_on_group_8 integer,
    axles_on_group_9 integer,
    speed double precision,
    gross_weight double precision,
    weight_axle_1 double precision,
    weight_axle_2 double precision,
    weight_axle_3 double precision,
    weight_axle_4 double precision,
    weight_axle_5 double precision,
    weight_axle_6 double precision,
    weight_axle_7 double precision,
    weight_axle_8 double precision,
    weight_axle_9 double precision,
    weight_group_1 double precision,
    weight_group_2 double precision,
    weight_group_3 double precision,
    weight_group_4 double precision,
    weight_group_5 double precision,
    weight_group_6 double precision,
    weight_group_7 double precision,
    distance_axle_1_2 double precision,
    distance_axle_2_3 double precision,
    distance_axle_3_4 double precision,
    distance_axle_4_5 double precision,
    distance_axle_5_6 double precision,
    distance_axle_6_7 double precision,
    distance_axle_7_8 double precision,
    distance_axle_8_9 double precision,
    valid_segmentation boolean DEFAULT true NOT NULL
);


ALTER TABLE ONLY acquisition ALTER COLUMN id SET DEFAULT nextval('acquisition_id_seq'::regclass);

ALTER TABLE ONLY acquisition_data
    ADD CONSTRAINT acquisition_data_pkey PRIMARY KEY (acquisition, time_seconds);

ALTER TABLE ONLY acquisition
    ADD CONSTRAINT acquisition_date_time_sensor_type_ukey UNIQUE (date_time, sensor_type);

ALTER TABLE ONLY acquisition
    ADD CONSTRAINT acquisition_pkey PRIMARY KEY (id);

ALTER TABLE ONLY acquisition_sensor_weigh
    ADD CONSTRAINT acquisition_sensor_weigh_pkey PRIMARY KEY (acquisition, num_sensor);

ALTER TABLE ONLY acquisition_data
    ADD CONSTRAINT acquisition_data_acquisition_fkey FOREIGN KEY (acquisition) REFERENCES acquisition(id);

ALTER TABLE ONLY acquisition_sensor_weigh
    ADD CONSTRAINT acquisition_sensor_weigh_acquisition_fkey FOREIGN KEY (acquisition) REFERENCES acquisition(id);
