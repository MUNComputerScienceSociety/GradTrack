var should = require('should');
var request = require('superagent');

describe('/departments', function () {
  it('should fetch a list of all departments.', function () {
    request.agent()
      .get('/courses/departments')
      .set('Accept', 'application/json')
      .end(function (err, res) {
        should.not.exist(err);
        should(res).have.property('length');
        should(res.length).be.greaterThan(0);
        should(res[0].length).be.equal(3);
      });
  });
});

describe('/:id', function () {
  it('should fetch a single course by its id', function () {
    request.agent()
      .get('/courses/0')
      .set('Accept', 'application/json')
      .end(function (err, res) {
        should.not.exist(err);
        should(res).have.property('id');
        should(res).have.property('departmentID');
        should(res).have.property('identifier');
        should(res).have.property('title');
        should(res).have.property('number');
        should(res).have.property('description');
      });
  });
});
