-- Run once in the project's SQL Editor. Safe to run again without deleting data.
begin;
create table if not exists public.user_progress (
  user_id uuid primary key references auth.users(id) on delete cascade,
  state jsonb not null check (coalesce((
    jsonb_typeof(state) = 'object'
    and state ->> 'app' = 'aca-practice'
    and state ->> 'schemaVersion' = '1'
    and jsonb_typeof(state -> 'drafts') = 'object'
    and jsonb_typeof(state -> 'attempts') = 'array'
  ), false)),
  revision bigint not null default 1 check (revision > 0),
  updated_at timestamptz not null default now()
);
alter table public.user_progress enable row level security;
revoke all on public.user_progress from anon, authenticated;
grant select on public.user_progress to authenticated;
drop policy if exists "Read own progress" on public.user_progress;
create policy "Read own progress" on public.user_progress for select to authenticated
  using ((select auth.uid()) = user_id);

-- Writes go through this function so every client must check the revision.
create or replace function public.save_progress(p_state jsonb, p_expected_revision bigint)
returns bigint language plpgsql security definer set search_path = '' as $$
declare
  owner_id uuid := auth.uid();
  saved_revision bigint;
begin
  if owner_id is null then
    raise exception 'Sign in to save progress' using errcode = '42501';
  end if;
  if p_state is null or octet_length(p_state::text) > 8388608
     or p_expected_revision is null or p_expected_revision < 0 then
    raise exception 'Invalid progress or revision' using errcode = '22023';
  end if;
  if p_expected_revision = 0 then
    insert into public.user_progress(user_id,state) values(owner_id,p_state)
      on conflict (user_id) do nothing returning revision into saved_revision;
  else
    update public.user_progress set state=p_state,revision=revision+1,updated_at=now()
      where user_id=owner_id and revision=p_expected_revision
      returning revision into saved_revision;
  end if;
  return saved_revision;
end;
$$;
revoke all on function public.save_progress(jsonb,bigint) from public, anon;
grant execute on function public.save_progress(jsonb,bigint) to authenticated;
commit;
