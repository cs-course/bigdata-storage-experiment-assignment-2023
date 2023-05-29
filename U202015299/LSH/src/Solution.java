import java.io.*;
import java.nio.channels.ClosedSelectorException;
import java.util.*;

class Locality_Sensitive_Hash{
    static class VectorUtils {
        private VectorUtils(){}

        static void print(int[] vec){
            if(vec==null){
                return;
            }
            else if(vec.length==0){
                System.out.print("[]");
                return;
            }
            System.out.print("[");
            for (int n:vec){
                System.out.print(n+",");
            }
            System.out.print("\b]");
        }
        static void println(int[] vec){
            print(vec);
            System.out.println();
        }

        @FunctionalInterface
        interface Distance_Function{
            int calc_dist(int [] Vec_A,int [] Vec_B);
        }
        static int Any_Distance(int[] vec_a, int[] vec_b, Distance_Function dist_func){
            if (vec_a==null||vec_b==null){throw new NullPointerException();}
            if (vec_a.length!=vec_b.length){throw new IllegalArgumentException();}
            if (vec_a.length==0){throw new ArrayIndexOutOfBoundsException();}
            return dist_func.calc_dist(vec_a,vec_b);
        }
        static int Manhattan_Distance(int [] vec_a,int [] vec_b){
            return Any_Distance(vec_a,vec_b,(a,b)->{
                int dist=0,len=a.length;
                for(int i=0;i<len;i++){
                    dist+=Math.abs(a[i]-b[i]);
                }
                return dist;
            });
        }

        static boolean[] concat(boolean[][] vectors){
            if (vectors==null){return null;}
            if (vectors.length==0||vectors[0].length==0){throw new IllegalArgumentException();}

            int I= vectors.length;
            int J= vectors[0].length;

            var ret=new boolean[I*J];
            for(int i=0,offset=0;i<I;i++,offset+=J){
                var row=vectors[i];
                if(row.length!=J){throw new IllegalArgumentException();}
                System.arraycopy(row, 0, ret, offset, J);
            }
            return ret;
        }
        static int compare(int [] vec_a,int [] vec_b){
            if (vec_a==null||vec_b==null){throw new NullPointerException();}
            if (vec_a.length!=vec_b.length){throw new IllegalArgumentException();}
            int len=vec_a.length;
            for(int i=0;i<len;i++){
                int delta=vec_a[i]-vec_b[i];
                if(delta!=0){return delta;}
            }
            return 0; // all components are the same
        }

        static String timeStamp(){
            var time=new Date(System.currentTimeMillis()).toString().split(" ");
            return time[1] + time[2];
        }
        static int[] randVec(int n,int max){
            if(n<1){throw new IllegalArgumentException();}
            var ret=new int[n];
            for(int i=0;i<n;i++){
                ret[i]=index_generator.nextInt(max);
            }
            return ret;
        }
    }
    static class Point implements Comparable<Point>{

        private final int[] coordinates;
        Point(int[] cartesian_coordinates){
            if(cartesian_coordinates==null||cartesian_coordinates.length!=vector_dimensions){throw new IllegalArgumentException();}
            coordinates= Arrays.copyOf(cartesian_coordinates,vector_dimensions);
        }
        Point(int val,int dim){coordinates=new int[dim];Arrays.fill(coordinates,0,dim,val);}

        <T> T map(Mapper<Point,T> mapper){
            return mapper.map(this);
        }
        int distance(Point p, VectorUtils.Distance_Function df){
            return df.calc_dist(coordinates,p.coordinates);
        }
        int[] getCoordinates() {
            return coordinates;
        }
        int getDimensions(){
            return coordinates.length;
        }
        void print (){
            VectorUtils.print(coordinates);
        }

        // Override for HashSet Distinction
        @Override
        public boolean equals(Object o) {
            if (this == o) return true;
            if (o == null || getClass() != o.getClass()) return false;
            Point point = (Point) o;
            return Arrays.equals(coordinates, point.coordinates);
        }
        @Override
        public int hashCode() {
            return 0;
        }
        @Override
        public int compareTo(Point o) {
            return VectorUtils.compare(coordinates,o.coordinates);
        }
        @Override
        public String toString(){
            var sb=new StringBuilder();
            for(int i:coordinates){
                sb.append(i);
                sb.append(" ");
            }
            return sb.toString();
        }
    }
    static class PointSet {

        private final HashSet<Point> points;
        private int max_value;

        void save(){
            try(var fr=new FileWriter(VectorUtils.timeStamp()+".ps");) {
                for(var p:points){
                    fr.write(p.toString());
                    fr.write("\n");
                }
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
        }
        void draw(Point q,Point[] neighbours,String FileName){
            if(vector_dimensions!=2){throw new UnsupportedOperationException();}
            enum status{
                IS_BLANK,
                IS_POINT,
                IS_TARGET,
                IS_NEIGHBOUR,
            }
            var graph=new status[max_value+1][max_value+1];
            for(int i=0;i<=max_value;i++){
                Arrays.fill(graph[i],0,max_value+1,status.IS_BLANK);
            }
            for(var p:points){
                var c=p.getCoordinates();
                graph[c[0]][c[1]]=status.IS_POINT;
            }
            for(var p:neighbours){
                var c=p.getCoordinates();
                graph[c[0]][c[1]]=status.IS_NEIGHBOUR;
            }
            var qc=q.getCoordinates();
            graph[qc[0]][qc[1]]=status.IS_TARGET;
            try(var fr=new FileWriter(FileName+".graph");) {
                for(var row:graph){
                    fr.write("|");
                    for(var col:row){
                        String todo=null;
                        switch (col){
                            case IS_TARGET -> todo="O";
                            case IS_POINT -> todo="*";
                            case IS_NEIGHBOUR -> todo="o";
                            case IS_BLANK -> todo=" ";
                        }
                        fr.write(todo);
                        fr.write(" ");
                    }
                    fr.write("|\n");
                }
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
        }
        static PointSet randomPointSet(int scale,int N){
            if(scale<1||N<1){throw new IllegalArgumentException();}
            var hs=new HashSet<Point>();
            while (hs.size()!=N){
                hs.add(new Point(VectorUtils.randVec(vector_dimensions,scale)));
            }
            var ret=new PointSet(hs,scale);
            ret.max_value=scale;
            return ret;
        }
        private PointSet(HashSet<Point> ps,int max){
            points=ps;
            max_value=max;
        }
        PointSet(String FilePath){
            try {
                FileReader fr=new FileReader(FilePath);
                BufferedReader br=new BufferedReader(fr);

                points=new HashSet<>();                       // vectors representing points
                max_value=Integer.MIN_VALUE;
                br.lines().forEach(s->{
                    var comps=s.split(" ");
                    if(comps.length<vector_dimensions){throw new IllegalArgumentException();}
                    int[] row=new int[vector_dimensions];
                    for(int i=0;i<vector_dimensions;i++){
                        int temp=Integer.parseInt(comps[i]);
                        max_value=Math.max(max_value,temp);
                        row[i]=temp;
                    }
                    points.add(new Point(row));
                });

                br.close();
                fr.close();
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
        }
        void show(){
            for (var p:points){
                VectorUtils.println(p.getCoordinates());
            }
        }
        int getMaxValue(){return max_value;}
        Set<Point> getPoints(){return points;}
        int size(){return points.size();};
    }
    @FunctionalInterface
    interface Mapper<F,T>{
        T map(F from);
    }
    static class HammingMapper implements Mapper<Point,boolean[]>{

        private final Mapper<Integer,boolean[]> Unary; // dealing with each component

        private HammingMapper(){
            Unary=x->{
                // assign: Top x digit as true, Lower (C-x) digits as false
                var ret=new boolean[component_length];
                Arrays.fill(ret,0,x,true);
                return ret;
            };
        }

        @Override
        public boolean[] map(Point p) {
            if(p==null||p.getCoordinates()==null||p.getDimensions()!=vector_dimensions){throw new IllegalArgumentException();}
            var vec=p.getCoordinates();
            int len=p.getDimensions();
            boolean[][] temp=new boolean[len][];
            for(int i=0;i<len;i++){
                temp[i]= Unary.map(vec[i]);
            }
            return VectorUtils.concat(temp); // connecting every component
        }
    }
    static class LSHFunctionCluster implements Mapper<boolean[],Integer>{

        private final Set<Integer> target_digits;

        LSHFunctionCluster(Set<Integer> targets){
            if(targets==null||targets.isEmpty()){throw new IllegalArgumentException();}
            target_digits=new HashSet<>(targets);
        }

        int size(){return target_digits.size();}

        @Override
        public Integer map(boolean[] ham_coordinates) {
            if(ham_coordinates.length!=hamming_coordinates_length){throw new IllegalArgumentException();}
            int index=0;
            for(int i:target_digits){
                index<<=1;
                if(ham_coordinates[i]){index+=1;}
            }
            return index;
        }
    }
    static class LSHFunctionGenerator{

        private final Set<Integer> rand_index_set=new HashSet<>();

        LSHFunctionCluster generate(){
            rand_index_set.clear();
            while (rand_index_set.size()<function_numbers){
                rand_index_set.add(index_generator.nextInt(hamming_coordinates_length));
            }
            return new LSHFunctionCluster(rand_index_set);
        }
    }
    static class LSHTable {

        private final HashMap<Integer,Set<Point>> table_contents;
        private final LSHFunctionCluster function_cluster;

        LSHTable(LSHFunctionCluster functions){
            if (functions==null||functions.size()==0){throw new IllegalArgumentException();}
            // preset init took too much heap space, wait until used
            table_contents= new HashMap<>();
            function_cluster =functions;
        }

        void put(Point p,boolean[] hamming_coordinates){
            table_contents.compute(function_cluster.map(hamming_coordinates),(Index,s)->{
                if(s==null){
                    s=new HashSet<>();
                    s.add(p);
                }
                else{
                    s.add(p);
                }
                return s;
            });
        }
        Set<Point> query(boolean[] hamming_coordinates){
            return table_contents.get(function_cluster.map(hamming_coordinates));
        }
    }

    static private final int MAX_FUNC_NUMS=30;

    static private int component_length;               // C
    static private int vector_dimensions;              // n
    static private int hamming_coordinates_length;     // n*C

    static private int function_numbers;               // K
    static private int table_numbers;                  // L

    private static final Random index_generator=
            new Random((( System.currentTimeMillis()%1000000007)
                            * (System.currentTimeMillis()%1000000021)) % 1000000033);
    private final LSHTable[] hash_tables;
    private final HammingMapper hamming_mapper;
    private final PointSet point_set;

    Locality_Sensitive_Hash(String ConfigFilePath,int scale,int percentage){
        try {
            if(percentage<1||percentage>=100){throw new IllegalArgumentException();}
            var pp=new Properties();
            var rd=new FileReader(ConfigFilePath);
            pp.load(rd);
            table_numbers=Integer.parseInt(pp.getProperty("HashTableNumbers"));
            function_numbers=Integer.parseInt(pp.getProperty("HashFunctionNumbers"));
            vector_dimensions=Integer.parseInt(pp.getProperty("VectorDimensions"));
            // hash table use int32 as index, each function has 2 status, the highest digit is sign digit
            if(table_numbers<1||function_numbers<1||function_numbers>MAX_FUNC_NUMS){throw new IllegalArgumentException();}

            point_set=PointSet.randomPointSet(scale,((scale*scale)*percentage)/100);

            component_length=point_set.getMaxValue();
            hamming_coordinates_length=component_length*vector_dimensions;

            hamming_mapper=new HammingMapper();
            var func_gen=new LSHFunctionGenerator();
            hash_tables=initialTables(func_gen);

            put(point_set);
            point_set.save();
            rd.close();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
    Locality_Sensitive_Hash(String ConfigFilePath){
        try {
            var pp=new Properties();
            var rd=new FileReader(ConfigFilePath);
            pp.load(rd);

            table_numbers=Integer.parseInt(pp.getProperty("HashTableNumbers"));
            function_numbers=Integer.parseInt(pp.getProperty("HashFunctionNumbers"));
            vector_dimensions=Integer.parseInt(pp.getProperty("VectorDimensions"));

            // hash table use int32 as index, each function has 2 status, the highest digit is sign digit
            if(table_numbers<1||function_numbers<1||function_numbers>MAX_FUNC_NUMS){throw new IllegalArgumentException();}

            String InputFilePath=pp.getProperty("InputFilePath");
            point_set=new PointSet(InputFilePath);

            component_length=point_set.getMaxValue();
            hamming_coordinates_length=component_length*vector_dimensions;

            hamming_mapper=new HammingMapper();
            var func_gen=new LSHFunctionGenerator();
            hash_tables=initialTables(func_gen);

            put(point_set);
            point_set.save();
            rd.close();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
    private LSHTable[] initialTables(LSHFunctionGenerator func_gen){
        var ret=new LSHTable[table_numbers];
        for(int i=0;i<table_numbers;i++){
            ret[i]= new LSHTable(func_gen.generate());
        }
        return ret;
    }

    private boolean using_silent_query=false;

    void speakUp(){using_silent_query=false;}
    void beQuite(){using_silent_query=true;}
    void showStatistics(boolean showDetail){
        System.out.println("point_set_size: "+point_set.size());
        System.out.println("table_numbers: "+table_numbers);
        System.out.println("function_numbers: "+function_numbers);
        System.out.println("vector_dimensions: "+vector_dimensions);

        int total_stored_points=table_numbers * point_set.size();
        int total_block_allocated=0;
        for(int i=0;i<table_numbers;i++){
            if (showDetail)System.out.println("In HashTable #"+i+":");
            var now = hash_tables[i];
            total_block_allocated+=now.table_contents.size();
            for(var e:now.table_contents.entrySet()){
                if (showDetail)System.out.println("row #"+e.getKey()+" carry "+e.getValue().size());
            }
        }
        if(showDetail)System.out.println("total_stored_points: "+total_stored_points);
        System.out.println("total_block_allocated: "+total_block_allocated);
    }
    void put(PointSet point_set){
        for(var p:point_set.points){
            var ham_coordinates=p.map(hamming_mapper);
            for(var ht:hash_tables){
                ht.put(p,ham_coordinates);
            }
        }
    }
    Point[] query(Point p,int n,int neg_weight){

        System.out.println();
        System.out.println("LSH Query:");
        System.out.println("using neglect_weight: "+neg_weight);

        long start_time=System.currentTimeMillis();

        var ham_coordinates=p.map(hamming_mapper);

        var candidates=new HashMap<Point,Integer[]>();
        int neg_tab=0,neg_p=0;
        for(var ht:hash_tables){
            if(neg_tab++==neg_weight){
                var tabQ=ht.query(ham_coordinates);
                if(tabQ==null){neg_tab=0;continue;}
                for(var pt:tabQ){
                    if(neg_p++==neg_weight){
                        candidates.compute(pt,(k,v)->{
                            if(v==null){
                                return new Integer[]{1,p.distance(k,VectorUtils::Manhattan_Distance)};
                            }
                            else {
                                v[0]++;
                                return v;
                            }
                        });
                        neg_p=0;
                    }
                }
                neg_tab=0;
            }
        }

        final int[] times_compare_point_rank = {0};
        final int[] times_compare_distance = {0};
        var entryList = new ArrayList<>(candidates.entrySet());
        entryList.sort((L,R)-> {
            // In Ascend Order
            var L_val=L.getValue();
            var R_val=R.getValue();
            int delta=R_val[0]-L_val[0];  // first calculate appear times
            if(delta==0){times_compare_distance[0]++;}
            delta=(delta==0)?
                    (R_val[1]-L_val[1]):
                    delta;
            delta=(delta==0)?       // if same: compare in dictionary order
                    (R.getKey().compareTo(L.getKey())):
                    delta;
            if (!using_silent_query)times_compare_point_rank[0]++;
            return delta;
        });// sorting rules
        long end_time=System.currentTimeMillis();
        System.out.println("total_time_used: "+(end_time-start_time));

        if (!using_silent_query){
            System.out.println("query_candidates_list_size: "+candidates.size());
            System.out.println("times_compare_point_rank: "+ times_compare_point_rank[0]);
            System.out.println("times_compare_distance: "+ times_compare_distance[0]);
        }

        var res=new Point[n];
        for(int i=0;i<n;i++){
            res[i]=entryList.get(i).getKey();
        }

        if(!using_silent_query)System.out.print("query_results: ");
        int total_distance=0;
        for(var neighbour:res){
            if(!using_silent_query){
                neighbour.print();
                System.out.print(" ");
            }
            total_distance+=p.distance(neighbour,VectorUtils::Manhattan_Distance);
        }
        if(!using_silent_query)System.out.println();
        System.out.println("total_distance: "+total_distance+", average_distance: "+(total_distance*1.0/n));

        return res;
    }
    Point[] accurate_search(Point p,int n){

        System.out.println();
        System.out.println("ACCURATE:");

        long start_time=System.currentTimeMillis();
        var hm=new HashMap<Point,Integer>();
        for(var candidate:point_set.getPoints()){
            hm.put(candidate,p.distance(candidate, VectorUtils::Manhattan_Distance));
        }

        final int[] times_compare_distance = {0};
        var entryList=new ArrayList<>(hm.entrySet());
        entryList.sort((L,R)-> {
            if (!using_silent_query)times_compare_distance[0]++;
            int delta=L.getValue()-R.getValue();
            delta=(delta==0)?(R.getKey().compareTo(L.getKey())):delta;
            return delta;
        });
        long end_time=System.currentTimeMillis();
        System.out.println("total_time_used: "+(end_time-start_time));
        if (!using_silent_query){
            System.out.println("times_calculate_distance: "+point_set.size());
            System.out.println("times_compare_distance: "+times_compare_distance[0]);
            System.out.print("query_results: ");}

        var res=new Point[n];
        int total_distance=0;
        for(int i=0;i<n;i++){
            var now=entryList.get(i);
            var neighbour=now.getKey();
            res[i]=neighbour;
            if(!using_silent_query){
                neighbour.print();
                System.out.print(" ");
            }
            total_distance+=now.getValue();
        }
        if(!using_silent_query)System.out.println();
        System.out.println("total_distance: "+total_distance+", average_distance: "+(total_distance*1.0/n));

        return res;
    }

    void draw(String FileName,Point[] neighbours,Point target){
        point_set.draw(target,neighbours,FileName);
    }
}

public class Solution {

    public static void main(String[] args) {
        //var lsh=new Locality_Sensitive_Hash("Config.properties");
        int test_scale=256;
        int pointsToScaleRatio=20;
        var lsh=new Locality_Sensitive_Hash("Config.properties",test_scale,pointsToScaleRatio);
        lsh.showStatistics(false);
        //lsh.beQuite();

        int query_result_scale=8;
        var test_point=new Locality_Sensitive_Hash.Point(test_scale/2,8);
        lsh.accurate_search(test_point,query_result_scale);
        lsh.query(test_point,query_result_scale,0);

//        lsh.draw("accurate",
//                lsh.accurate_search(test_point,query_result_scale),
//                test_point);
//        lsh.draw("LSH",
//                lsh.query(test_point,query_result_scale,1),
//                test_point);

    }

}