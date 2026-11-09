import assert from 'node:assert/strict';
import {isNoneOption,pinNoneLast,shuffleOptions} from '../core.mjs';
const opts=[
  {id:'a',text:'None of the answers A)–D) is correct.'},
  {id:'b',text:'Cost of capital rises.'},
  {id:'c',text:'None of the above'},
  {id:'d',text:'Equity falls.'},
];
assert.equal(isNoneOption(opts[0]),true);
assert.equal(isNoneOption(opts[1]),false);
assert.equal(isNoneOption({text:'Almost none of the firms report.'}),false);
for(let i=0;i<50;i++){
  const order=shuffleOptions(opts);
  assert.deepEqual(order.slice(2).sort(),['a','c']);
  assert.equal(new Set(order).size,4);
}
assert.deepEqual(pinNoneLast(['a','b','c','d'],opts),['b','d','a','c']);
assert.deepEqual(pinNoneLast(['c','b','a','d'],opts),['b','d','c','a']);
console.log('none-last tests passed');
