# mt-manage-cli

`mt-manage-cli` adalah antarmuka baris perintah (CLI) yang digunakan untuk mengelola berbagai layanan seperti akun SSH, Noobzvpn, dan Xray. Selain itu, CLI ini juga menyediakan server web API untuk mengelola akun melalui permintaan HTTP.

---

## Penggunaan CLI

| Command | Deskripsi |
|--|--|
| `ssh` | Mengelola akun SSH |
| `noobzvpn` | Mengelola akun Noobzvpn |
| `vmess` | Mengelola akun VMess |
| `vless` | Mengelola akun VLess |
| `trojan` | Mengelola akun Trojan |
| `shadowsocks` | Mengelola akun Shadowsocks |
| `serve` | Menjalankan server API Web |
| `run` | Menjalankan tugas wajib di background |

| Action | Req_Options |
|--|--|
| `add` | Semua opsi |
| `edit` | `-e`, `-d`, `-b` |
| `remove` | `--user` |
| `lock` | `--user` |
| `unlock` | `--user` |
| `detail` | `--user` |

| Options | Informasi | For_Command | default_value |
|--|--|--|--|
| `--types` | Tipe link untuk akun Xray (`all`/`ws`/`grpc`) | untuk Xray (`vmess`, `vless`, `trojan`, `shadowsocks`) | all |
| `--user` | Username untuk semua layanan | Untuk Xray (`vmess`, `vless`, `trojan`, `shadowsocks`) | |
| `--pass` | Password untuk akun | untuk `ssh` & `noobzvpn` | |
| `--uuid` | UUID [v4] untuk akun | untuk Xray (`vmess`, `vless`, `trojan`, `shadowsocks`) | random |
| `-e` | Tanggal kadaluarsa | untuk semua layanan | 360 |
| `-d` | Batas perangkat | untuk semua layanan | 0 |
| `-b` | Batas bandwidth | untuk semua layanan | 0 |

### Menampilkan Bantuan
Menampilkan bantuan umum untuk CLI:
```bash
./mt-manage-cli --help
```
Menampilkan bantuan untuk service:
```bash
./mt-manage-cli <command> --help
```
Menampilkan bantuan untuk Aksi service:
```bash
./mt-manage-cli <command> <action> --help
```

---

### Penggunaan

```USAGE
Usage: ./mt-manage-cli [command] [action] [opts]

[command]:
ssh [action] [..] : Mengelola akun SSH.
noobzvpn [action] [..] : Mengelola akun Noobzvpn.
vmess [action] [..] : Mengelola akun VMess.
vless [action] [..] : Mengelola akun VLess.
trojan [action] [..] : Mengelola akun Trojan.
shadowsocks [action] [..] : Mengelola akun Shadowsocks.
serve [opts] [..] : Menjalankan server API Web.
run [..] : Menjalankan tugas wajib di background.

[action]:
add [opts] [..] : Menambah akun baru.
edit [opts] [..] : Mengedit akun yang sudah ada.
remove [opts] [..] : Menghapus akun yang sudah ada.
lock [opts] [..] : Mengunci akun yang sudah ada.
unlock [opts] [..] : Membuka kunci akun yang sudah ada.
detail [opts] [..] : Mendapatkan detail akun yang sudah ada.

[opts]:
--types <TYPE_XRAY> : Menentukan tipe link akun Xray, default: all.
--user <USERNAME> : Menentukan username akun.
--pass <PASSWORD> : Menentukan password akun.
--uuid <UUID V4> : Menentukan UUID akun, default: random.
-e, <DAYS> : Menentukan masa kadaluarsa akun, default: 360 hari.
-d, <UNITS> : Menentukan batas perangkat maksimal, default: 0 (unlimited).
-b, <GIGA_BYTES> : Menentukan batas bandwidth, default: 0 (unlimited).
```

---

### Contoh Penggunaan Perintah

#### SSH
- Menambah akun SSH:
  ```bash
  ./mt-manage-cli ssh add --user <username> --pass <password> -e <expiration_date> -d <device_limit> -b <bandwidth_limit>
  ```
- Mengedit akun SSH

  semua opsi :
  ```bash
  ./mt-manage-cli ssh edit --user <username> --pass <password> -e <expiration_date> -d <device_limit> -b <bandwidth_limit>
  ```
  
  hanya opsi tertentu :
  ```bash
  ./mt-manage-cli ssh edit --user <username> -e <expiration_date> 
  ```
- Menghapus akun SSH
  ```bash
  ./mt-manage-cli ssh remove --user <username>
  ```
- Mengunci akun SSH
  ```bash
  ./mt-manage-cli ssh lock --user <username>
  ```
- Membuka kunci akun SSH
  ```bash
  ./mt-manage-cli ssh unlock --user <username>
  ```
- Mendapatkan detail akun SSH
  ```bash
  ./mt-manage-cli ssh detail --user <username>
  ```

#### Noobzvpns
- Menambah akun Noobzvpn
  ```bash
  ./mt-manage-cli noobzvpn add --user <username> --pass <password> -e <expiration_date> -d <device_limit> -b <bandwidth_limit>
  ```
- Mengedit akun Noobzvpn

  semua opsi :
  ```bash
  ./mt-manage-cli noobzvpn edit --user <username> --pass <password> -e <expiration_date> -d <device_limit> -b <bandwidth_limit>
  ```
  
  hanya opsi tertentu :
  ```bash
  ./mt-manage-cli noobzvpn edit --user <username> -e <expiration_date> 
  ```
- Menghapus akun Noobzvpn
  ```bash
  ./mt-manage-cli noobzvpn remove --user <username>
  ```
- Mengunci akun Noobzvpn
  ```bash
  ./mt-manage-cli noobzvpn lock --user <username>
  ```
- Membuka kunci akun Noobzvpn
  ```bash
  ./mt-manage-cli noobzvpn unlock --user <username>
  ```
- Mendapatkan detail akun Noobzvpn
  ```bash
  ./mt-manage-cli noobzvpn detail --user <username>
  ```

#### Xray ( vmess, vless, trojan, shadowsocks )
- Menambah akun Xray
  ```bash
  ./mt-manage-cli vmess add --user <username> --uuid <uuid> -e <expiration_date> -d <device_limit> -b <bandwidth_limit>
  ```
  
- Mengedit akun Xray

  semua opsi :
  ```bash
  ./mt-manage-cli vmess edit --user <username> --uuid <uuid> -e <expiration_date> -d <device_limit> -b <bandwidth_limit>
  ```
  
  hanya opsi tertentu :
  ```bash
  ./mt-manage-cli vmess edit --user <username> -e <expiration_date> 
  ```
- Menghapus akun Xray
  ```bash
  ./mt-manage-cli vmess remove --user <username>
  ```
- Mengunci akun Xray
  ```bash
  ./mt-manage-cli vmess lock --user <username>
  ```
- Membuka kunci akun Xray
  ```bash
  ./mt-manage-cli vmess unlock --user <username>
  ```
- Mendapatkan detail akun Xray
  ```bash
  ./mt-manage-cli vmess detail --user <username>
  ```

> Catatan: Gantilah vmess dengan vless, trojan, atau shadowsocks jika Anda ingin menggunakan layanan tersebut dengan perintah yang sama.

---

### Penggunaan API
Berikut ini adalah contoh penggunaan dan bagaimana cara memanggil endpoint untuk menambahkan akun melalui API `mt-manage-cli`:

- Contoh `config.json`
```json
{
    "apikey": "<api_key>"
    "port": 2052,
    "token": "<bot_token>",
    "admin": [
      "<id_tele>",
      "xxx"
    ],
    "ip": "xxx-ip",
    "isp": "xxx-isp",
    "city": "xxx-city",
    "manage": {
        "ip_action": "lock",
        "quota_action": "remove",
        "interval": 300
    }
}
```

| Service       | Endpoint                       | HTTP Method | Description                    |
|---------------|--------------------------------|-------------|--------------------------------|
| ssh, noobzvpn, vmess, vless, trojan, shadowsocks | `/add`                           | POST        | Menambahkan akun baru untuk layanan tertentu |
| ssh, noobzvpn, vmess, vless, trojan, shadowsocks | `/edit`                          | PATCH       | Mengedit akun yang ada untuk layanan tertentu |
| ssh, noobzvpn, vmess, vless, trojan, shadowsocks | `/remove`                        | DELETE      | Menghapus akun dari layanan tertentu |
| ssh, noobzvpn, vmess, vless, trojan, shadowsocks | `/lock`                          | POST        | Mengunci akun untuk layanan tertentu |
| ssh, noobzvpn, vmess, vless, trojan, shadowsocks | `/unlock`                        | POST        | Membuka kunci akun untuk layanan tertentu |
| ssh, noobzvpn, vmess, vless, trojan, shadowsocks | `/detail`                        | GET         | Mendapatkan detail lengkap dari akun untuk layanan tertentu |
| ssh, noobzvpn, vmess, vless, trojan, shadowsocks | `/accounts`                      | GET         | Mendapatkan jumlah total dari akun-akun untuk layanan tertentu |

> **Note:** Gantilah `{service}` di URL dengan salah satu layanan berikut: `ssh`, `noobzvpn`, `vmess`, `vless`, `trojan`, atau `shadowsocks`.

---

## Petunjuk Penggunaan API

Berikut adalah rangkuman langkah-langkah yang perlu dilakukan:

1. **Menjalankan Server:**
   Pastikan server sudah berjalan dengan menjalankan perintah:
   ```bash
   ./mt-manage-cli serve
   ```

2. **Mengirim Permintaan:**
   Gunakan `curl`, Postman, atau alat lainnya untuk mengirim permintaan POST ke endpoint yang telah ditentukan.

   - **Menambahkan Akun SSH:**
     ```bash
     curl -X POST http://localhost:2052/ssh/add -H "Content-Type: application/json" -H "Authorization: Bearer <api_key>" -d '{ "user": "username", "pass": "password", "exp": "360", "device": "999", "bandwidth": "9999" }'
     ```

   - **Menambahkan Akun Noobzvpn:**
     ```bash
     curl -X POST http://localhost:2052/noobzvpn/add -H "Content-Type: application/json" -H "Authorization: Bearer <api_key>" -d '{ "user": "username", "pass": "password", "exp": "360", "device": "999", "bandwidth": "9999" }'
     ```

   - **Menambahkan Akun Xray:**
     ```bash
     curl -X POST http://localhost:2052/vmess/add -H "Content-Type: application/json" -H "Authorization: Bearer <api_key>" -d '{ "types": "all", "user": "username", "uuid": "random", "exp": "360", "device": "999", "bandwidth": "9999" }'
     ```

3. **Respon JSON:**
   Setiap permintaan yang berhasil akan menghasilkan respon dalam format JSON seperti yang telah dijelaskan sebelumnya.

   Contoh respon JSON untuk masing-masing layanan:

   - **SSH:**
     ```json
     {
         "status": "success",
         "result": {
             "service": "ssh",
             "user": "username",
             "pass": "password",
             "iplim": "999",
             "quota": "9999",
             "status": "unlock",
             "exp_date": "360"
         },
         "config": {
             "domain": "example.com",
             "nsdomain": "ns.example.com",
             "pubkey": "public_key_string",
             "port": {
                 "ntls": [80, 8080],
                 "tls": 443,
                 "slowdns": [443, 53, 88],
                 "udpcustom": "54-65535",
                 "dropbear": 143,
                 "openvpn": [1194, 2200, 443],
                 "squid": 3128,
                 "badvpn": [7100, 7200, 7300]
             }
         },
         "message": "Successfully added ssh account for user: username"
     }
     ```

   - **Noobzvpn:**
     ```json
     {
         "status": "success",
         "result": {
             "service": "noobzvpn",
             "user": "username",
             "pass": "password",
             "iplim": "999",
             "quota": "9999",
             "status": "unlock",
             "exp_date": "360"
         },
         "config": {
             "domain": "example.com",
             "port": {
                 "ntls": 8880,
                 "tls": 8443
             }
         },
         "message": "Successfully added noobzvpn account for user: username"
     }
     ```

   - **Xray:**
     ```json
     {
         "status": "success",
         "result": {
             "service": "xray",
             "types": "vmess",
             "user": "username",
             "uuid": "uuid",
             "iplim": 999,
             "quota": 9999,
             "status": "unlock",
             "exp_date": "2023-07-25"
         },
         "config": {
             "domain": "example.com",
             "port": {
                 "tls": 443,
                 "ntls": 80,
                 "grpc": 8848
             },
             "link": {
                 "tls": "link_tls",
                 "ntls": "link_ntls",
                 "grpc": "link_grpc"
             },
             "path": {
                 "ws": "path_ws",
                 "grpc": "path_grpc",
             }
         },
         "message": "Successfully added xray account for user: username"
     }
     ```

### Contoh Endpoint Lainnya
Anda juga bisa menggunakan endpoint lain seperti mengedit, menghapus, mengunci / membuka kunci akun, mendapatkan detail akun, dan. total akun.

Contoh permintaan untuk menghapus akun:
```bash
curl -X <method> http://localhost:2052/<service>/<action> -H "Content-Type: application/json" -H "Authorization: Bearer <api_key>" -d '{ "user": "username" }'
```

Respon jika permintaan berhasil:
```json
{
    "message": "Successfully removed <service> account for user: username",
    "status": "success"
}
```

Respon jika user tidak ada:
```json
{
    "message": "User username does not exist.",
    "status": "error"
}
```

---

### Lisensi
Proyek ini dilisensikan di bawah MIT License. Lihat file [LICENSE](LICENSE) untuk informasi lebih lanjut.

---
