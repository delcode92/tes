create table pegawai ( id serial primary key, rfid_pegawai varchar(30),nama_pegawai varchar(50) );

insert into pegawai(rfid_pegawai, nama_pegawai) values ('0014832825', 'razi');
insert into pegawai(rfid_pegawai, nama_pegawai) values ('0014832822', 'santi');
insert into pegawai(rfid_pegawai, nama_pegawai) values ('0014532811', 'budi');
insert into pegawai(rfid_pegawai, nama_pegawai) values ('0017732811', 'ani');
insert into pegawai(rfid_pegawai, nama_pegawai) values ('0014832811', 'susi');
insert into pegawai(rfid_pegawai, nama_pegawai) values ('0018832811', 'anton');
insert into pegawai(rfid_pegawai, nama_pegawai) values ('0014800811', 'nana');

CREATE TABLE users (id serial primary key, username varchar(100), user_level varchar(80), password varchar(255));
insert into users(username, user_level, password) values ('andi', 'pegawai', '123');
insert into users(username, user_level, password) values ('susi', 'kasir', '123456');
insert into users(username, user_level, password) values ('budi', 'kasir', '1256');


CREATE TABLE rfid (id serial primary key, rfid varchar(100), nama varchar(80) );
insert into rfid(rfid, nama) values ('0014832825', 'razi');
insert into rfid(rfid, nama) values ('0014222825', 'budi');
insert into rfid(rfid, nama) values ('0014442825', 'susi');


-- CREATE TABLE kasir (
--     id serial primary key, 
--     nik varchar(100), 
--     nama varchar(80), 
--     hp varchar(15), 
--     alamat varchar(255), 
--     jm_masuk varchar(10), 
--     jm_keluar varchar(10), 
--     no_pos varchar(10)
-- );

CREATE TABLE kasir ( id serial primary key, nik varchar(100), nama varchar(80), hp varchar(15), alamat varchar(255), jm_masuk varchar(10), jm_keluar varchar(10), no_pos varchar(10) );
insert into kasir (nik, nama, hp, alamat, jm_masuk, jm_keluar, no_pos) values ('111223344', 'susi', '085263636', 'darussalam', '08:00', '12:00', '1');insert into kasir (nik, nama, hp, alamat, jm_masuk, jm_keluar, no_pos) values ('1144523344', 'budi', '0852636234', 'darussalam', '12:00', '18:00', '1');
 

CREATE TABLE gate ( id serial primary key, no_pos varchar(10), tipe_pos varchar(30), jns_kendaraan varchar(50), ip_cam varchar(60) );
insert into gate (no_pos, tipe_pos, jns_kendaraan, ip_cam) values ('1', 'masuk', 'motor', '192.168.100.10#192.168.100.12');
insert into gate (no_pos, tipe_pos, jns_kendaraan, ip_cam) values ('1', 'keluar', 'motor', '192.168.100.16#192.168.100.18');

CREATE TABLE tarif ( id serial primary key, no_pos varchar(10), tarif_perjam serial, tarif_per24jam serial, jns_kendaraan varchar(50) );
insert into tarif (no_pos, tarif_perjam, tarif_per24jam, jns_kendaraan) values ('1', 1000, 4000, 'motor');
insert into tarif (no_pos, tarif_perjam, tarif_per24jam, jns_kendaraan) values ('1', 2000, 8000, 'mobil');

-- 05012023 091305 993320
-- CREATE TABLE clients_socket ( id integer NOT NULL, ip character varying(20) NOT NULL, port integer NOT NULL );
CREATE TABLE clients_socket ( id serial primary key, ip character varying(20) NOT NULL, port integer NOT NULL );


-- id|barcode|date_time|gate|images_path 
create table pegawai ( id serial primary key, rfid_pegawai varchar(30),nama_pegawai varchar(50) );
CREATE TABLE karcis ( id serial primary key, barcode varchar(150), datetime timestamp(6) with time zone, gate varchar(20), images_path varchar(255), status_parkir BOOLEAN NOT NULL DEFAULT FALSE, jenis_kendaraan varchar(30), ip_raspi varchar(25) );

insert into karcis (datetime) values(to_timestamp(1672912953.570569));
insert into karcis (barcode, datetime, gate, jenis_kendaraan) values ('3127192', '2023-02-05 15:02:12', '2', 'mobil');

CREATE TABLE tes ( id serial primary key, barcode varchar(150), datetime timestamp(6) with time zone, gate varchar(20), images_path varchar(255), jns_kendaraan varchar(20) );
insert into tes (barcode, datetime, gate, jns_kendaraan) values ('12313123', '2023-02-05 15:02:12', '1', 'motor');

CREATE TABLE voucher ( id serial primary key, id_pel varchar(30), lokasi varchar(255), tarif serial, masa_berlaku date, jns_kendaraan varchar(20) );
CREATE TABLE laporan_users ( id serial primary key, barcode varchar(30), ket varchar(255) );