var should = require('should');

module.exports = function () {
  should(5).be.exactly(5);
  should(3).be.greaterThan(2);
};
