var should = require('should');
var request = require('superagent');


var baseURL = 'http://localhost:3000/';

describe('courses/departments', function () {
  var agent = request.agent();

  it('should fetch a list of all departments.', function (done) {
    agent
      .get(baseURL + 'courses/departments')
      .set('Accept', 'application/json')
      .end(function (err, res) {
        should.not.exist(err);
        res = JSON.parse(res.text);
        should.not.exist(res.error);
        res = res.data;
        res.should.have.property('length');
        res.length.should.be.greaterThan(0);
        res[0].should.have.property('id');
        res[0].should.have.property('name');
        res[0].should.have.property('identifier');
        done();
      });
  });
});

describe('courses/:id', function () {
  var agent = request.agent();

  it('should fetch a single course by its id', function (done) {
    agent
      .get(baseURL + 'courses/1')
      .set('Accept', 'application/json')
      .end(function (err, res) {
        should.not.exist(err);
        res = JSON.parse(res.text);
        should.not.exist(res.error);
        res = res.data;
        res.should.have.property('id');
        res.should.have.property('department_id');
        res.should.have.property('identifier');
        res.should.have.property('title');
        res.should.have.property('number');
        res.should.have.property('description');
        done();
      });
  });
});
