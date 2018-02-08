---
title: ember-unit-test
date: 2016-06-28 01:28:21
tags:
- JavaScript
- Unit Test
- Ember
---

Testing is a core part of the Ember framework and its development cycle.

### Test framework

- [QUnit](https://qunitjs.com/)
- [PhantomJs](http://phantomjs.org/)

### How to run

Under `js_app/frontend/` folder:
- `ember test`: run tests
- `ember test --test-page='tests/index.html?coverage=true'`: run tests with coverage
- `rake coverage:js`: runt tests with coverage
- `ember test -filter 'test des'`: run one test what des is 'test des'
- `ember test --server`: run tests and e-run tests on every file-change
- `ember server;  localhost:4200/test`: run tests on server

<!--more-->
### Test helpers

#### `moduleFor(fullName [, description [, callbacks]])`

- `fullName`: (String) - The full name of the unit, ie
  `controller:application`, `route:index`.

- `description`: (String) optional - The description of the module

- `callbacks`: (Object) optional
   - QUnit callbacks (`beforeEach` and `afterEach`)
   - ember-test-helpers callback (`subject`)
   - `integration: true` or `unit: true` (default: `integration: true`)
   - `needs` specify any dependencies the tested module will require.

#### `moduleForComponent(name, [description, callbacks])`

- `name`: (String) - the short name of the component that you'd use in a
  template, ie `x-foo`, `ic-tabs`, etc.

- `description`: (String) optional - The description of the module

- `callbacks`: (Object) optional
   - QUnit callbacks (`beforeEach` and `afterEach`)
   - ember-test-helpers callback (`subject`)
   - `integration: true` or `unit: true` (default: `integration: true`)
   - `needs` specify any dependencies the tested module will require.  (Including this will force your test into unit mode).


#### `moduleForModel(name, [description, callbacks])`

- `name`: (String) - the short name of the model you'd use in `store`
  operations ie `user`, `assignmentGroup`, etc.

- `description`: (String) optional - The description of the module

- `callbacks`: (Object) optional
   - QUnit callbacks (`beforeEach` and `afterEach`)
   - ember-test-helpers callback (`subject`)
   - `integration: true` or `unit: true` (default: `integration: true`)
   - `needs` specify any dependencies the tested module will require.

### Test Model
[Ember Guide](http://guides.emberjs.com/v1.13.0/testing/testing-models/)

```js
import { test, moduleForModel } from 'ember-qunit';
import Ember from 'ember';

moduleForModel('user','some des', {
  needs: ['model:child']
});

test('It can set its child', function(assert) {
  assert.expect(1);
  var subject = this.subject();

  Ember.run(()={
    var child = subject.store.createRecord('child');
    subject.get('children').pushObject(child);
  })

  assert.equal(subject.get('some-computed-value'), true);
});
```

### Test controllers

If there is a controller:
```js
export default Ember.Controller.extend({

  propA: 'You need to write tests',
  propB: 'And write one for me too',

  setPropB: function(str) {
    this.set('propB', str);
  },

  actions: {
    setProps: function(str) {
      this.set('propA', 'Testing is cool');
      this.setPropB(str);
    }
  }
});
```
Test code
```js
test('calling the action setProps updates props A and B', function(assert) {
  assert.expect(4);

  // get the controller instance
  var ctrl = this.subject();

  // check the properties before the action is triggered
  assert.equal(ctrl.get('propA'), 'You need to write tests');
  assert.equal(ctrl.get('propB'), 'And write one for me too');

  // trigger the action on the controller by using the `send` method,
  // passing in any params that our action may be expecting
  Ember.run(()={
   ctrl.send('setProps', 'Testing Rocks!');
  });

  // finally we assert that our values have been updated
  // by triggering our action.
  assert.equal(ctrl.get('propA'), 'Testing is cool');
  assert.equal(ctrl.get('propB'), 'Testing Rocks!');
});
```

```js
import { test, moduleForComponent } from 'ember-qunit';

moduleForComponent('x-foo', {
  unit: true,
  needs: ['helper:pluralize-string']
});

// run a test
test('it renders', function(assert) {
  assert.expect(1);

  // creates the component instance
  var subject = this.subject();

  // render the component on the page
  this.render();
  assert.equal(this.$('.foo').text(), 'bar');
});
```
```js
test('sometimes async gets rejected', function(assert) {
  assert.expect(1);
  var myThing = MyThing.create()

  return myThing.exampleMethod().then(function() {
    assert.ok(false, "promise should not be fulfilled");
  })['catch'](function(err) {
    assert.equal(err.message, "User not Authorized");
  });
});
```
