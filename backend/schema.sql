-- Minimal schema for AutoAppDev controller state.

create table if not exists app_config (
  key text primary key,
  value jsonb not null,
  updated_at timestamptz not null default now()
);

create table if not exists chat_messages (
  id bigserial primary key,
  role text not null,
  content text not null,
  created_at timestamptz not null default now()
);

create table if not exists inbox_messages (
  id bigserial primary key,
  role text not null,
  content text not null,
  created_at timestamptz not null default now()
);

create table if not exists pipeline_runs (
  id bigserial primary key,
  status text not null,
  pid integer,
  started_at timestamptz not null default now(),
  stopped_at timestamptz,
  script text not null,
  cwd text not null,
  args jsonb not null default '[]'::jsonb
);

create table if not exists pipeline_state (
  id integer primary key,
  state text not null,
  pid integer,
  run_id bigint,
  started_at timestamptz,
  paused_at timestamptz,
  resumed_at timestamptz,
  stopped_at timestamptz,
  updated_at timestamptz not null default now()
);

insert into pipeline_state(id, state) values (1, 'stopped') on conflict (id) do nothing;
