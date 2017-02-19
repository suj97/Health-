drop table if exists login_credentials;
create table login_credentials (
  username char(32) primary key,
  password char(32) not null
);

insert into login_credentials (username, password) values ('roby','roby');