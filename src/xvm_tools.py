def calc_check_sum(msg):
    num = msg.find(";*") + 1
    calc = 0
    for i in range(num):
        calc ^= ord(msg[i])
    return calc


def parse_xvm(msg):
    xvmMessage = msg.split(";")
    message = xvmMessage[0]
    id = xvmMessage[1][3:]
    sequence = int(xvmMessage[2][1:], 16)
    checksum = int(xvmMessage[3][1:3], 16)
    return (message, id, sequence, checksum)


def generate_ack(id, sequence):
    resp = ">ACK;ID=" + id + ";#" + format(sequence, "04X") + ";*"
    resp = resp + format(calc_check_sum(resp), "02X") + "<\r\n"
    return resp


def generate_xvm(id, sequence, message):
    resp = message + ";ID=" + id + ";#" + sequence + ";*"
    resp = resp + format(calc_check_sum(resp), "02X") + "<\r\n"
    return resp


def is_valid_xvm(msg):
    return 1 if calc_check_sum(msg) == parse_xvm(msg)[3] else 0
