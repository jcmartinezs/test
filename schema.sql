drop table if exists entries;
create table entries (
  name text primary key,
  fvcolor text not null,
  pet text not null
);
