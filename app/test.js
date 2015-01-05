var fs = require('fs');

fs.readdir('./tests', function (err, files) {
  if (err) {
    console.log('Could not open tests directory.');
  } else {
    for (var i = 0, len = files.length; i < len; i++) {
      if (files[i].substring(files[i].length - 3, files[i].length) === '.js') {
        console.log('Running test function from ' + files[i]);
        require('./tests/' + files[i].substring(0, files[i].length - 3))();
      }
    }
  }
});
