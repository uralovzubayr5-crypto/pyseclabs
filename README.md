# PySecLabs

Hands-on offensive-security lab pack from my teaching years at an IT academy in
Tashkent: a vulnerable VM, 20 guided exercises, and an auto-grader for the Python
capstones.

Built by [Zubayr Uralov](https://github.com/uralovzubayr5-crypto).

## What is inside

| path | what it is |
|---|---|
| `labs/Vagrantfile` | one-command vulnerable VM (Ubuntu + deliberately weak services) |
| `labs/bootstrap.sh` | provisions the intentionally-vulnerable services |
| `exercises/01-recon.md` … `20-report.md` | guided exercises, each with a flag to capture |
| `exercises/capstones/` | Python automation assignments (port scanner, log parser, report generator) |
| `grader/` | runs a student script in a sandbox and scores its output |

## Quick start (instructor)

```sh
cd labs
vagrant up          # first boot takes ~10 minutes
vagrant ssh         # credentials are in the exercise sheet, not on GitHub
```

## Quick start (student)

```sh
pip install -r grader/requirements.txt
python grader/grade.py exercises/capstones/port_scanner.py --rubric exercises/capstones/rubrics/port_scanner.yaml
```

The grader executes the student's script inside a Docker network that can only see the
lab VM, so a runaway scanner cannot leave the classroom.

## Exercise map

```
01 recon & OSINT        05 web basics          09 password attacks
02 nmap & services      06 injection          10 privilege escalation (linux)
03 python automation    07 file uploads       11 privesc (windows)
04 report writing       08 auth bypass        12–20 capstones & exam
```

## Why it is public

Students learn faster when the lab is reproducible and the grader is not a black box.
The vulnerable services are intentionally tied to the VM's internal network; do not
deploy `labs/` anywhere reachable from the internet.

## License

MIT (course text CC BY-SA 4.0)
