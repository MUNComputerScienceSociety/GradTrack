var Mocha = require('mocha');
var fs = require('fs');
var path = require('path');
var config = require('./config');

var mocha = new Mocha();
fs.readdirSync(config.testsDir).filter(function (filename) {
  return filename.substr(-3) === '.js';
}).forEach(function (filename) {
  mocha.addFile(path.join(config.testsDir, filename));
});

mocha.run(function (failures) {
  process.on('exit', function () {
    process.exit(failures);
  });
});
