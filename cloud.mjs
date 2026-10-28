import {mergeBackups} from './core.mjs';

export const progressKey = (base,userId) => userId ? `${base}:user:${userId}` : base;

// A revision check makes a stale device re-read and merge before it can write.
export function createProgressSync({client,getState,applyState,validate,onStatus}){
  let userId=null,epoch=0,changes=0,timer=null,running=null,restoreRemote=false;
  const current=e=>e===epoch&&userId!==null;
  const status=(e,message)=>{if(current(e))onStatus(message);};
  async function sync(e,id){
    try{
      status(e,'Syncing progress…');
      for(let retry=0;retry<4;retry++){
        const {data:remote,error}=await client.from('user_progress').select('state,revision').eq('user_id',id).maybeSingle();
        if(!current(e))return false;
        if(error)throw error;
        const local=getState(),incoming=remote?validate(remote.state):null;
        const merged=incoming?mergeBackups(local,incoming):local;
        if(incoming){
          if(restoreRemote&&changes===0)Object.assign(merged,{session:local.session||incoming.session,preferences:incoming.preferences,view:incoming.view});
          else merged.session=local.session;
        }
        restoreRemote=false;
        applyState(merged);
        const version=changes,payload=structuredClone(getState());
        const {data:revision,error:writeError}=await client.rpc('save_progress',{
          p_state:payload,p_expected_revision:remote?.revision??0,
        });
        if(!current(e))return false;
        if(writeError)throw writeError;
        if(revision===null)continue;
        if(version!==changes)continue;
        status(e,'Saved to your account');
        return true;
      }
      throw new Error('Progress changed on another device. Try Sync now again.');
    }catch(error){
      status(e,`Cloud save failed. Your browser copy is kept. ${error.message||'Check your connection and try again.'}`);
      return false;
    }
  }
  function flush(){
    clearTimeout(timer);
    if(!userId)return Promise.resolve(true);
    if(running)return running;
    const e=epoch;
    const task=sync(e,userId).finally(()=>{if(e===epoch)running=null;});
    running=task;
    return task;
  }
  return {
    setUser(id,restore=false){clearTimeout(timer);epoch++;userId=id;changes=0;running=null;restoreRemote=restore;},
    schedule(){
      if(!userId)return;
      changes++;
      onStatus('Saved in this browser. Waiting to sync…');
      clearTimeout(timer);timer=setTimeout(flush,1200);
    },
    flush,
  };
}
