"-H" s_enable_hexdump = [no | yes]
"-S" s_ssi_pattern  = #.html
"-a" freopen
"-d" s_root_dir     = .
"-g" s_tun_enable   = [no | false]
"-i" s_iid          = randomlow()
"-l" s_listening_address = http://0.0.0.0:8000
"-t" s_tun_server   = wss://dashboard.mongoose.ws/ws
"-u" s_tun_pass
"-v" s_debug_level  = [2 | 0 | 3]

"-h" usage

-e  quit
