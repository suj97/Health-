drop table if exists login_credentials;
create table login_credentials (
  username char(32) primary key,
  password char(32) not null
);

insert into login_credentials (username, password) values ('roby','roby');
insert into login_credentials (username, password) values ('sujay','sujay');

drop table if exists details;
create table details (
  username char(32) primary key,
  patient_name char(32) default "Not Registered", 
  patient_age char(32) default "Not Registered",
  patient_sex char(32) default "Not Registered",
  patient_blood_group char(32) default "Not Registered",
  patient_weight char(32) default "Not Registered",
  patient_contact char(32) default "Not Registered"
);

insert into details (username, patient_name, patient_age, patient_sex, patient_blood_group, patient_weight, patient_contact) values ('roby','Onkar Singh', '21', 'M' , 'O+' , '76' , '9816926947');


drop table if exists appointments;
create table appointments (
	username char(32) primary key,
	name char(32) not null,
	email char(32) not null,
	booking_date char(32) not null,
	department char(32) not null
);