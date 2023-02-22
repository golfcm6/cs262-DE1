#!/bin/bash
echo starting unit tests
sleep 1
echo creating test_output files

python3 -u server.py 127.0.0.1 > server_output.txt &
PID1=$!
sleep 1
# testing shit
# https://serverfault.com/questions/188936/writing-to-stdin-of-background-process
rm /tmp/srv-input
mkfifo /tmp/srv-input
cat > /tmp/srv-input &
echo $! > /tmp/srv-input-cat-pid
tail -f /tmp/srv-input | python3 client.py 127.0.0.1 > client1_output.txt &
printf 'c\n|\nash\n' > /tmp/srv-input
sleep 1
printf 'u\nash\nc\ncharles\n2\nash\n2\nb\n2\n*.\n3\nash\nhello!\n2\n\nexit\n' | python3 client.py 127.0.0.1 > client2_output.txt &
PID3=$!
sleep 1
printf 'exit\n' > /tmp/srv-input
sleep 1
printf 'u\nbob\nu\nash\n3\ncharles\ngoodbye\n3\nlol\ninvalid account\n4\n' | python3 client.py 127.0.0.1 > client3_output.txt &
PID4=$!
sleep 1
printf 'u\ncharles\nexit\n' | python3 client.py 127.0.0.1 > client4_output.txt &
PID5=$!
sleep 1

# now do some test to verify that the outputs of files are correct
# thx https://stackoverflow.com/questions/12900538/fastest-way-to-tell-if-two-files-have-the-same-contents-in-unix-linux
echo checking output files
cmp --silent client1_output.txt client1_expected.txt || echo "client1 differences"
cmp --silent client2_output.txt client2_expected.txt || echo "client1 differences"
cmp --silent client3_output.txt client3_expected.txt || echo "client1 differences"
cmp --silent client4_output.txt client4_expected.txt || echo "client1 differences"

echo all tests passed!
kill $PID1
exit 0
