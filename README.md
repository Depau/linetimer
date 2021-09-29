# Line timer

Times stdout/stderr lines of a subprocess:

```
$ ./linetime.py bash -c 'echo hello; sleep 1; echo world 1>&2; sleep 0.5; date'
[out 0:00:00.002277] hello
[err 0:00:01.002972] world
[out 0:00:01.504103] Wed Sep 29 04:57:25 PM CEST 2021
```

## License

MIT