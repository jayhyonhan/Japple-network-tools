#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <netinet/ip.h>
#include <netinet/tcp.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <netinet/ip.h>
#include <netinet/tcp.h>
#include <time.h>

void send_syn_packet(const char* dst_ip, unsigned short dst_port, size_t packet_size) {
    int sockfd;
    struct sockaddr_in target_addr;
    struct iphdr ip_header;
    struct tcphdr tcp_header;
    char packet[IP_MAXPACKET];

    sockfd = socket(AF_INET, SOCK_RAW, IPPROTO_RAW);
    if (sockfd == -1) {
        perror("Socket creation error");
        exit(1);
    }

    memset(&target_addr, 0, sizeof(struct sockaddr_in));
    target_addr.sin_family = AF_INET;
    target_addr.sin_port = htons(dst_port);
    target_addr.sin_addr.s_addr = inet_addr(dst_ip);

    ip_header.ihl = 5;
    ip_header.version = 4;
    ip_header.tos = 0;
    ip_header.tot_len = sizeof(struct iphdr) + sizeof(struct tcphdr) + packet_size;
    ip_header.id = htons(12345);
    ip_header.frag_off = 0;
    ip_header.ttl = 64;
    ip_header.protocol = IPPROTO_TCP;
    ip_header.check = 0; // Вычисление чексуммы
    ip_header.saddr = inet_addr("YOUR_SOURCE_IP");
    ip_header.daddr = target_addr.sin_addr.s_addr;

    tcp_header.source = htons(12345);
    tcp_header.dest = htons(dst_port);
    tcp_header.seq = random(); // Задайте правильное значение
    tcp_header.ack_seq = 0;
    tcp_header.doff = sizeof(struct tcphdr) / 4;
    tcp_header.syn = 1;
    tcp_header.window = htons(65535);
    tcp_header.check = 0; // Вычисление чексуммы
    tcp_header.urg_ptr = 0;

    memcpy(packet, &ip_header, sizeof(struct iphdr));
    memcpy(packet + sizeof(struct iphdr), &tcp_header, sizeof(struct tcphdr));

    for (size_t i = sizeof(struct iphdr) + sizeof(struct tcphdr); i < ip_header.tot_len; ++i) {
        packet[i] = rand() % 256;
    }

    if (sendto(sockfd, packet, ip_header.tot_len, 0, (struct sockaddr*)&target_addr, sizeof(struct sockaddr)) == -1) {
        perror("Packet sending error");
        exit(1);
    }

    close(sockfd);
}

int main() {
    char target_ip[16];
    unsigned short target_port;
    size_t packet_size;

    printf("Enter the target IP address: ");
    scanf("%15s", target_ip);

    printf("Enter the target port: ");
    scanf("%hu", &target_port);

    printf("Enter the packet size in bytes: ");
    scanf("%lu", &packet_size);

    srand(time(NULL));

    send_syn_packet(target_ip, target_port, packet_size);

    return 0;
}
